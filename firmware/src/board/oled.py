"""Driver I2C mínimo SSD1306 128x64; protocolo conforme MicroPython/SSD1306."""

import framebuf


class Oled(framebuf.FrameBuffer):
    def __init__(self, bus, address=0x3C):
        self.bus = bus
        self.address = address
        self.buffer = bytearray(1024)
        super().__init__(self.buffer, 128, 64, framebuf.MONO_VLSB)
        for command in (
            0xAE, 0x20, 0x00, 0x40, 0xA1, 0xA8, 63, 0xC8,
            0xD3, 0x00, 0xDA, 0x12, 0xD5, 0x80, 0xD9, 0xF1,
            0xDB, 0x30, 0x81, 0xFF, 0xA4, 0xA6, 0x8D, 0x14, 0xAF,
        ):
            self.bus.writeto(address, bytes((0x80, command)))
        self.fill(0)
        self.show()

    def show(self):
        for command in (0x21, 0, 127, 0x22, 0, 7):
            self.bus.writeto(self.address, bytes((0x80, command)))
        # Prefixo de dados; buffer reutilizado entre quadros.
        self.bus.writevto(self.address, (b"\x40", self.buffer))
