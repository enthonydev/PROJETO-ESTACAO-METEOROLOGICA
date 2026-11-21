"""Bancada MicroPython: mesma pinagem Arduino; pressão exclusivamente DEMO."""

import math


class Station:
    DHT_MS = 2000
    INPUT_MS = 200
    OLED_MS = 200
    DIAGNOSTIC_MS = 5000
    OLED_RETRY_MS = 5000
    PRESSURE_CYCLES = 200

    def __init__(self, dht, rain, light, clock, random_bits, oled_factory, log=print):
        self.dht = dht
        self.rain = rain
        self.light = light
        self.clock = clock
        self.random_bits = random_bits
        self.oled_factory = oled_factory
        self.log = log
        self.oled = None
        self.temperature = None
        self.humidity = None
        self.pressure_demo = None
        self.pressure_cycles = 0
        self.raining = None
        self.dark = None
        self.online = False
        now = clock.ticks_ms()
        self.last_dht = now
        self.last_inputs = now
        self.last_oled = now
        self.last_diagnostic = now
        self.last_oled_retry = now
        self._read_dht()
        self._read_inputs()
        self._open_oled()
        self._draw()
        self.log("[DEMO] Apenas a pressao e simulada; mudanca a cada 200 ciclos.")
        self.log("[SISTEMA] Estacao MicroPython iniciada. Ctrl+C para o terminal USB.")

    def _read_dht(self):
        try:
            self.dht.measure()
            temperature = self.dht.temperature()
            humidity = self.dht.humidity()
            if not (
                math.isfinite(temperature) and math.isfinite(humidity)
                and -40 <= temperature <= 80 and 0 <= humidity <= 100
            ):
                raise ValueError("DHT fora da faixa")
            self.temperature, self.humidity = temperature, humidity
            # Formato compatível com tools/serial_bridge.py, sem misturar DEMO.
            self.log("Temperatura: %.1f C | Umidade: %.1f %%" % (temperature, humidity))
        except (OSError, ValueError, RuntimeError):
            self.temperature = self.humidity = None
            self.log("[ERRO] Falha na leitura do DHT22!")

    def _read_inputs(self):
        raining = self.rain.value() == 0
        dark = self.light.value() == 1
        if raining != self.raining:
            self.raining = raining
            self.log("Chuva: " + ("DETECTADA" if raining else "NAO DETECTADA"))
        if dark != self.dark:
            self.dark = dark
            self.log("Luminosidade: " + ("ESCURO" if dark else "CLARO"))

    def _pressure_tick(self):
        self.pressure_cycles += 1
        if self.pressure_demo is not None and self.pressure_cycles < self.PRESSURE_CYCLES:
            return
        self.pressure_cycles = 0
        self.pressure_demo = (10220 + self.random_bits(16) % 21) / 10.0
        self.log("[SIMULADO] Pressao DEMO: %.1f hPa" % self.pressure_demo)

    def _open_oled(self):
        try:
            self.oled = self.oled_factory()
        except OSError:
            self.oled = None
            self.log("[ERRO] OLED indisponivel; sensores e USB continuam.")

    def _draw(self):
        if self.oled is None:
            return
        try:
            screen = self.oled
            screen.fill(0)
            screen.text("ESTACAO", 36, 0)
            screen.text("METEOROLOGICA", 12, 10)
            screen.hline(0, 19, 128, 1)
            screen.text("T:--" if self.temperature is None else "T:%.1f C" % self.temperature, 0, 22)
            screen.text("U:--" if self.humidity is None else "U:%.1f %%" % self.humidity, 0, 32)
            pressure = "P DEMO:--" if self.pressure_demo is None else "P DEMO:%.1fhPa" % self.pressure_demo
            screen.text(pressure, 0, 42)
            screen.text("CH:" + ("S" if self.raining else "N"), 0, 54)
            screen.text("L:" + ("E" if self.dark else "C"), 48, 54)
            screen.text("W:" + ("S" if self.online else "N"), 96, 54)
            screen.show()
        except OSError:
            self.oled = None
            self.log("[ERRO] Falha I2C na OLED; sensores e USB continuam.")

    def step(self, online=False):
        now = self.clock.ticks_ms()
        self.online = online
        due = lambda previous, interval: self.clock.ticks_diff(now, previous) >= interval
        if due(self.last_dht, self.DHT_MS):
            self.last_dht = now
            self._read_dht()
            self._pressure_tick()
        if due(self.last_inputs, self.INPUT_MS):
            self.last_inputs = now
            self._read_inputs()
        if due(self.last_diagnostic, self.DIAGNOSTIC_MS):
            self.last_diagnostic = now
            self.log("[DIAGNOSTICO] Chuva GPIO17: %s | Interpretacao: %s" % (
                "LOW" if self.raining else "HIGH",
                "AGUA DETECTADA" if self.raining else "SEM AGUA DETECTADA",
            ))
        if self.oled is None and due(self.last_oled_retry, self.OLED_RETRY_MS):
            self.last_oled_retry = now
            self._open_oled()
        if due(self.last_oled, self.OLED_MS):
            self.last_oled = now
            self._draw()
