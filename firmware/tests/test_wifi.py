"""Exercita a lógica Wi-Fi com relógio e interface WLAN simulados."""

import pytest

from services.wifi import WifiConnection, load_profiles


class Clock:
    now = 0

    def ticks_ms(self):
        return self.now

    def ticks_add(self, ticks, delta):
        return (ticks + delta) % 128

    def ticks_diff(self, a, b):
        return (a - b + 64) % 128 - 64


class Wlan:
    online = False

    def __init__(self):
        self.calls = []

    def active(self, enabled):
        self.calls.append(("active", enabled))

    def config(self, *, reconnects):
        assert reconnects == 0

    def connect(self, ssid, password=None):
        self.calls.append(("connect", ssid, password))

    def disconnect(self):
        self.calls.append(("disconnect",))
        self.online = False

    def isconnected(self):
        return self.online


def test_timeout_switches_profile_across_clock_wrap_then_reconnects():
    clock = Clock()
    clock.now = 120
    wlan = Wlan()
    wifi = WifiConnection(wlan, [("first", "key"), ("second", "")], clock, 10, 5)

    assert not wifi.poll()
    assert wlan.calls[-1] == ("connect", "first", "key")
    clock.now = 1
    assert not wifi.poll()
    assert wlan.calls[-1] == ("connect", "first", "key")
    clock.now = 2
    assert not wifi.poll()
    assert wlan.calls[-1] == ("disconnect",)
    clock.now = 6
    assert not wifi.poll()
    assert wlan.calls[-1] == ("disconnect",)
    clock.now = 7
    assert not wifi.poll()
    assert wlan.calls[-1] == ("connect", "second", None)
    wlan.online = True
    assert wifi.poll()
    assert wifi.poll()

    wlan.online = False
    assert not wifi.poll()
    assert wlan.calls[-2:] == [("disconnect",), ("connect", "first", "key")]
    wlan.online = True
    assert wifi.poll()


def test_driver_error_waits_before_trying_next_profile(monkeypatch):
    clock = Clock()
    wlan = Wlan()
    connect = wlan.connect

    def fail_first(ssid, password=None):
        if ssid == "first":
            raise OSError("falha simulada")
        connect(ssid, password)

    monkeypatch.setattr(wlan, "connect", fail_first)
    wifi = WifiConnection(wlan, [("first", "key"), ("second", "key")], clock, 10, 5)
    assert not wifi.poll()
    clock.now = 4
    assert not wifi.poll()
    assert wlan.calls[-1] == ("disconnect",)
    clock.now = 5
    assert not wifi.poll()
    assert wlan.calls[-1] == ("connect", "second", "key")


def test_missing_profile_file_leaves_radio_untouched(tmp_path):
    profiles = load_profiles(str(tmp_path / "wifi_profiles.json"))
    wlan = Wlan()
    assert not WifiConnection(wlan, profiles, Clock()).poll()
    assert wlan.calls == []


def test_local_profiles_are_loaded_in_order(tmp_path):
    path = tmp_path / "wifi_profiles.json"
    path.write_text('[{"ssid":"first","password":"key"},{"ssid":"second","password":""}]')
    assert load_profiles(str(path)) == (("first", "key"), ("second", ""))
    path.write_text('[{"ssid":"first"}]')
    with pytest.raises(ValueError, match="Perfil Wi-Fi inválido"):
        load_profiles(str(path))


def test_usb_interrupt_returns_from_wifi_loop(monkeypatch, capsys):
    import sys
    import time
    from types import SimpleNamespace

    from main import run_wifi
    from services import wifi

    wlan = Wlan()
    clock = Clock()

    def interrupt(_milliseconds):
        raise KeyboardInterrupt

    monkeypatch.setitem(sys.modules, "network", SimpleNamespace(STA_IF=0, WLAN=lambda _: wlan))
    monkeypatch.setattr(wifi, "load_profiles", lambda: (("first", "key"),))
    monkeypatch.setattr(time, "ticks_ms", clock.ticks_ms, raising=False)
    monkeypatch.setattr(time, "ticks_diff", clock.ticks_diff, raising=False)
    monkeypatch.setattr(time, "ticks_add", clock.ticks_add, raising=False)
    monkeypatch.setattr(time, "sleep_ms", interrupt, raising=False)

    run_wifi()

    assert wlan.calls[-1] == ("connect", "first", "key")
    assert capsys.readouterr().out == ""
