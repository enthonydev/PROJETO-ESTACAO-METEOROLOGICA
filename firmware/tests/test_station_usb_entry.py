"""O loop de bancada permanece interrompível por Ctrl+C na USB."""
import sys
import time
from types import SimpleNamespace
from main import run_station
from firmware.tests.test_board_station import Clock,Dht,Pin,Screen
from firmware.tests.test_wifi import Wlan

def test_station_keyboard_interrupt_returns_to_usb(monkeypatch,capsys):
    from services import wifi
    clock=Clock(); wlan=Wlan()
    class HardwarePin(Pin):
        IN=0; PULL_UP=2
        def __init__(self,*args): pass
    class I2C:
        def __init__(self,**kwargs): pass
        def scan(self): return [0x3c]
    monkeypatch.setitem(sys.modules,'machine',SimpleNamespace(Pin=HardwarePin,SoftI2C=I2C))
    monkeypatch.setitem(sys.modules,'network',SimpleNamespace(STA_IF=0,WLAN=lambda _:wlan))
    monkeypatch.setitem(sys.modules,'dht',SimpleNamespace(DHT22=lambda pin:Dht()))
    monkeypatch.setitem(sys.modules,'board.oled',SimpleNamespace(Oled=lambda bus:Screen()))
    monkeypatch.setattr(wifi,'load_profiles',lambda:(('rede','senha'),))
    monkeypatch.setattr(time,'ticks_ms',clock.ticks_ms,raising=False)
    monkeypatch.setattr(time,'ticks_diff',clock.ticks_diff,raising=False)
    monkeypatch.setattr(time,'ticks_add',clock.ticks_add,raising=False)
    def stop(ms): raise KeyboardInterrupt
    monkeypatch.setattr(time,'sleep_ms',stop,raising=False)
    run_station()
    out=capsys.readouterr().out
    assert 'Temperatura: 21.3 C | Umidade: 82.2 %' in out
    assert 'Terminal USB disponivel' in out
    assert 'senha' not in out
