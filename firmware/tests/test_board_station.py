"""Agendamento e falhas de bancada sem ESP32 físico."""
from board.station import Station
from services.wifi import WifiConnection

class Clock:
    now = 0
    period = 1 << 30
    def ticks_ms(self): return self.now % self.period
    def ticks_diff(self, a, b): return (a-b+self.period//2)%self.period-self.period//2
    def ticks_add(self, a, delta): return (a+delta)%self.period

class Dht:
    calls = 0
    fail = False
    def measure(self):
        self.calls += 1
        if self.fail: raise OSError('sensor ausente')
    def temperature(self): return 21.3
    def humidity(self): return 82.2

class Pin:
    level = 1
    def value(self): return self.level

class Screen:
    fail = False
    def __init__(self): self.frames=[]; self.pending=[]
    def fill(self, value): self.pending=[]
    def hline(self, *args): pass
    def text(self, text, x, y):
        assert x+len(text)*8 <= 128 and y+8 <= 64
        self.pending.append(text)
    def show(self):
        if self.fail: raise OSError('I2C')
        self.frames.append(self.pending[:])

def make_station(factory=None):
    clock,dht,rain,light,screen=Clock(),Dht(),Pin(),Pin(),Screen()
    logs=[]
    station=Station(dht,rain,light,clock,lambda bits:123,factory or (lambda:screen),logs.append)
    return station,clock,dht,rain,light,screen,logs

def test_pressure_first_period_then_only_after_200_more_cycles():
    station,clock,dht,_,_,screen,logs=make_station()
    assert station.pressure_demo is None
    clock.now=2000; station.step()
    assert 1022 <= station.pressure_demo <= 1024
    assert sum(line.startswith('[SIMULADO]') for line in logs)==1
    for i in range(2,201): clock.now=i*2000; station.step()
    assert sum(line.startswith('[SIMULADO]') for line in logs)==1
    clock.now=201*2000; station.step()
    assert sum(line.startswith('[SIMULADO]') for line in logs)==2
    assert dht.calls==202
    assert any(any('P DEMO:' in text for text in frame) for frame in screen.frames)
    assert 'Temperatura: 21.3 C | Umidade: 82.2 %' in logs

def test_dht_failure_does_not_stop_inputs_display_or_demo():
    station,clock,dht,rain,light,screen,logs=make_station()
    dht.fail=True; rain.level=light.level=0
    clock.now=2000; station.step(online=True)
    assert station.temperature is None and station.humidity is None
    assert station.raining and not station.dark and station.pressure_demo is not None
    assert 'Chuva: DETECTADA' in logs and 'Luminosidade: CLARO' in logs
    assert 'W:S' in screen.frames[-1] and 'T:--' in screen.frames[-1]
    dht.fail=False; clock.now=4000; station.step()
    assert station.temperature==21.3

def test_oled_disconnect_recovers_without_restarting_sensors():
    station,clock,dht,_,_,screen,logs=make_station()
    screen.fail=True; clock.now=200; station.step()
    assert station.oled is None
    screen.fail=False; clock.now=5000; station.step()
    assert station.oled is screen and dht.calls==2
    assert any('Falha I2C' in line for line in logs)

def test_no_oled_at_start_does_not_block_reads():
    def missing(): raise OSError('sem OLED')
    station,clock,dht,*_=make_station(missing)
    clock.now=2000; station.step()
    assert dht.calls==2 and station.oled is None

def test_clock_wrap_preserves_dht_interval():
    station,clock,dht,*_=make_station()
    station.last_dht=clock.period-1000
    clock.now=999; station.step(); assert dht.calls==1
    clock.now=1000; station.step(); assert dht.calls==2

def test_offline_wifi_does_not_block_sensor_updates():
    from firmware.tests.test_wifi import Wlan
    clock=Clock(); wlan=Wlan()
    wifi=WifiConnection(wlan,[('rede-a','senha'),('rede-b','')],clock,5000,1000)
    station,_,dht,*_=make_station(); station.clock=clock
    for now in range(0,16001,200): clock.now=now; station.step(wifi.poll())
    assert dht.calls==9
    assert len([call for call in wlan.calls if call[0]=='connect'])>=2
    wlan.online=True; clock.now=18000; station.step(wifi.poll())
    assert station.online and dht.calls==10
