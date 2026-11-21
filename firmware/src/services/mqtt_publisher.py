"""Publicador MQTT 3.1.1 QoS 0 cooperativo, sem dependencias externas.

Broker IPv4 local, sem TLS; uso na rede privada de demonstracao.
Nao publica pressao DEMO nem converte entradas digitais em mm/porcentagem.
"""
import asyncio
import json
import time


def load_config(path='mqtt_config.json'):
    try:
        with open(path) as f:
            data = json.load(f)
    except OSError:
        return None
    if not data.get('enabled', False):
        return None
    host = data.get('host', '')
    pieces = host.split('.')
    if len(pieces) != 4 or not all(p.isdigit() and 0 <= int(p) <= 255 for p in pieces):
        raise ValueError('Broker deve usar IPv4, evitando consulta DNS no loop.')
    port = data.get('port', 1883)
    if not isinstance(port, int) or not 1 <= port <= 65535:
        raise ValueError('Porta MQTT invalida')
    station = data.get('station_id', 'estacao-esp32-real')
    if not station or any(x in station for x in '/+#\x00'):
        raise ValueError('station_id invalido')
    return {'host': host, 'port': port, 'station_id': station,
            'username': data.get('username'), 'password': data.get('password')}


def mqtt_string(value):
    raw = value.encode('utf-8')
    if len(raw) > 65535:
        raise ValueError('Texto MQTT muito longo')
    return bytes((len(raw) >> 8, len(raw) & 255)) + raw


def frame(header, body):
    size = len(body)
    remaining = bytearray()
    while True:
        digit = size % 128
        size //= 128
        remaining.append(digit | (128 if size else 0))
        if not size:
            break
    return bytes((header,)) + bytes(remaining) + body


def connect_frame(config):
    flags = 2  # Clean session, sem Will.
    payload = mqtt_string(config['station_id'])
    username = config.get('username')
    password = config.get('password')
    if password is not None and username is None:
        raise ValueError('Senha MQTT exige usuario')
    if username is not None:
        flags |= 128
        payload += mqtt_string(username)
    if password is not None:
        flags |= 64
        payload += mqtt_string(password)
    return frame(0x10, b'\x00\x04MQTT\x04' + bytes((flags, 0, 30)) + payload)


def telemetry(station, station_id, utc):
    if utc[0] < 2025:
        raise ValueError('Relogio UTC nao sincronizado')
    return {
        'schema_version': '1.0', 'station_id': station_id,
        'timestamp': '%04d-%02d-%02dT%02d:%02d:%02dZ' % tuple(utc[:6]),
        'location': {'latitude': None, 'longitude': None},
        'measurements': {
            'temperature_c': station.temperature, 'humidity_pct': station.humidity,
            'pressure_hpa': None, 'air_quality_raw': None,
            'luminosity_pct': None, 'rain_mm': None,
        },
        'quality': {
            'temperature': 'ok' if station.temperature is not None else 'error',
            'humidity': 'ok' if station.humidity is not None else 'error',
            'pressure': 'error', 'air_quality': 'error',
            'luminosity': 'error', 'rain': 'error',
        },
    }


class Publisher:
    def __init__(self, config, online, get_payload, log=print, interval=2,
                 retry=5, timeout=3):
        self.config = config
        self.online = online
        self.get_payload = get_payload
        self.log = log
        self.interval, self.retry, self.timeout = interval, retry, timeout

    async def run(self):
        while True:
            writer = None
            try:
                if not self.online():
                    await asyncio.sleep(.2)
                    continue
                # Sem relogio UTC valido, nao transmite timestamps inventados.
                self.get_payload()
                reader, writer = await asyncio.wait_for(
                    asyncio.open_connection(self.config['host'], self.config['port']), self.timeout)
                writer.write(connect_frame(self.config))
                await asyncio.wait_for(writer.drain(), self.timeout)
                ack = await asyncio.wait_for(reader.readexactly(4), self.timeout)
                if ack != b'\x20\x02\x00\x00':
                    raise OSError('CONNACK recusado ou invalido')
                self.log('[MQTT] Conectado ao broker.')
                topic = 'estacao/' + self.config['station_id'] + '/telemetry'
                while self.online():
                    data = self.get_payload()
                    body = mqtt_string(topic) + json.dumps(data).encode('utf-8')
                    writer.write(frame(0x30, body))  # QoS 0, nao retido.
                    await asyncio.wait_for(writer.drain(), self.timeout)
                    self.log('[MQTT] Publicado QoS0: ' + topic + ' | ' + data['timestamp'])
                    # Envios a cada 2 s mantem a sessao ativa (< keepalive 30 s).
                    await asyncio.sleep(self.interval)
            except (OSError, ValueError, asyncio.TimeoutError, EOFError) as exc:
                self.log('[MQTT] Indisponivel: ' + str(exc) + '; nova tentativa. USB/OLED continuam.')
            finally:
                if writer is not None:
                    writer.close()
                    try:
                        await asyncio.wait_for(writer.wait_closed(), self.timeout)
                    except (OSError, asyncio.TimeoutError):
                        pass
            await asyncio.sleep(self.retry)


async def run_station_mqtt(station, wifi, wlan, config, log=print):
    publisher = Publisher(config, lambda: station.online,
                          lambda: telemetry(station, config['station_id'], time.gmtime()), log)
    task = asyncio.create_task(publisher.run())
    connected = False
    try:
        while True:
            online = wifi.poll()
            station.step(online)
            if online != connected:
                connected = online
                log('[WIFI] Conectado. IP: ' + wlan.ifconfig()[0] if online
                    else '[WIFI] Desconectado; reconexao automatica ativa.')
            await asyncio.sleep(.02)
    finally:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass
