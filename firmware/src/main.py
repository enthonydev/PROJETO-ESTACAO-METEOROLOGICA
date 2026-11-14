"""Firmware MicroPython da bancada, mantendo os serviços da arquitetura."""

from services.connectivity import Connectivity
from services.sensor_service import SensorService
from services.time_service import TimeService
from services.weather_api import WeatherStateService


class FirmwareApplication:
    """Agrupa serviços por injeção de dependências para futura integração física."""

    def __init__(
        self,
        sensor_drivers=None,
        weather_provider=None,
        primary_time_source=None,
        fallback_time_source=None,
    ):
        self.sensor_service = SensorService(sensor_drivers)
        self.weather_service = WeatherStateService(weather_provider)
        self.time_service = TimeService(primary_time_source, fallback_time_source)
        self.connectivity = Connectivity()

    def read_local_state(self):
        return self.sensor_service.read()


def run_wifi():
    import network
    import time

    from services.wifi import WifiConnection, load_profiles

    try:
        profiles = load_profiles()
    except (ValueError, OSError):
        print("Wi-Fi: configuração local inválida ou inacessível")
        return
    if not profiles:
        print("Wi-Fi: sem perfis configurados")
        return

    wlan = network.WLAN(network.STA_IF)
    wifi = WifiConnection(wlan, profiles, time)
    connected = False
    try:
        while True:
            online = wifi.poll()
            if online != connected:
                print("Wi-Fi: conectado" if online else "Wi-Fi: desconectado")
                connected = online
            time.sleep_ms(100)
    except KeyboardInterrupt:
        pass




def run_station():
    """Execução física integrada; não aguarda Wi-Fi para ler sensores."""
    import time
    import random
    import network
    import dht
    from machine import Pin, SoftI2C
    from board.oled import Oled
    from board.station import Station
    from services.wifi import WifiConnection, load_profiles

    bus = SoftI2C(sda=Pin(21), scl=Pin(22), freq=100000, timeout=20000)
    try:
        addresses = bus.scan()
        for address in addresses:
            print("[I2C] Encontrado: 0x%02X" % address)
        print("[I2C] Total de dispositivos: %d" % len(addresses))
        if not any(address in addresses for address in (0x76, 0x77)):
            print("[I2C] Nenhuma resposta em 0x76 ou 0x77. Pressao DEMO independente.")
    except OSError:
        print("[I2C] Falha na varredura; funcionamento sem OLED sera tentado.")
    try:
        profiles = load_profiles()
    except (ValueError, OSError):
        print("[WIFI] Configuracao invalida; bancada continua sem rede.")
        profiles = ()
    if not profiles:
        print("[WIFI] Sem perfis; bancada continua sem rede.")
    wlan = network.WLAN(network.STA_IF)
    wifi = WifiConnection(wlan, profiles, time)
    station = Station(
        dht.DHT22(Pin(16)), Pin(17, Pin.IN, Pin.PULL_UP),
        Pin(5, Pin.IN), time, random.getrandbits, lambda: Oled(bus),
    )
    connected = False
    try:
        while True:
            online = wifi.poll()
            station.step(online)
            if online != connected:
                connected = online
                if online:
                    print("[WIFI] Conectado. IP: " + wlan.ifconfig()[0])
                else:
                    print("[WIFI] Desconectado; reconexao automatica ativa.")
            time.sleep_ms(20)
    except KeyboardInterrupt:
        print("[SISTEMA] Loop interrompido. Terminal USB disponivel.")


if __name__ == "__main__":
    run_station()
