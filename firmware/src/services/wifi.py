"""Associação Wi-Fi em etapas, sem esperar pela rede no loop do firmware."""

import json


def load_profiles(path="/wifi_profiles.json"):
    try:
        with open(path) as config:
            profiles = json.load(config)
    except OSError as error:
        if error.args[0] == 2:  # ENOENT: bancada sem configuração Wi-Fi
            return ()
        raise

    if not isinstance(profiles, list):
        raise ValueError("Configuração Wi-Fi deve ser uma lista de perfis")
    for profile in profiles:
        if (
            not isinstance(profile, dict)
            or not isinstance(profile.get("ssid"), str)
            or not profile["ssid"]
            or not isinstance(profile.get("password"), str)
        ):
            raise ValueError("Perfil Wi-Fi inválido")
    return tuple((profile["ssid"], profile["password"]) for profile in profiles)


class WifiConnection:
    """Alterna entre perfis por ordem e volta a tentar após perda de conexão."""

    def __init__(self, wlan, profiles, clock, timeout_ms=15000, retry_ms=5000):
        self._wlan = wlan
        self._profiles = profiles
        self._clock = clock
        self._timeout_ms = timeout_ms
        self._retry_ms = retry_ms
        self._next_profile = 0
        self._active = False
        self._connecting = False
        self._connected = False
        self._deadline = clock.ticks_ms()

    def poll(self):
        """Avança uma etapa e informa se a estação tem IP."""
        if not self._profiles:
            return False

        now = self._clock.ticks_ms()
        try:
            if self._active and self._wlan.isconnected():
                self._connecting = False
                self._connected = True
                return True

            if self._connected:
                self._connected = False
                self._wlan.disconnect()
                self._deadline = now

            if self._clock.ticks_diff(now, self._deadline) < 0:
                return False

            if self._connecting:
                self._schedule_retry(now)
                return False

            if not self._active:
                self._wlan.active(True)
                self._wlan.config(reconnects=0)
                self._active = True
            ssid, password = self._profiles[self._next_profile]
            self._next_profile = (self._next_profile + 1) % len(self._profiles)
            self._connecting = True
            if password:
                self._wlan.connect(ssid, password)
            else:
                self._wlan.connect(ssid)
            self._deadline = self._clock.ticks_add(now, self._timeout_ms)
        except OSError:
            self._schedule_retry(now)
        return False

    def _schedule_retry(self, now):
        self._connected = False
        self._connecting = False
        self._deadline = self._clock.ticks_add(now, self._retry_ms)
        if self._active:
            try:
                self._wlan.disconnect()
            except OSError:
                # Se o driver falhar ao cancelar, reinicialize na próxima tentativa.
                self._active = False
