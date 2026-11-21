import asyncio
import json
from types import SimpleNamespace
import pytest
from services.mqtt_publisher import Publisher,telemetry,frame,connect_frame,load_config

CFG={'host':'127.0.0.1','port':1883,'station_id':'estacao-esp32-real'}
S=SimpleNamespace(temperature=23.1,humidity=86.3,pressure_demo=1023)
UTC=(2026,11,14,5,0,0,5,318)

def test_payload_real_only_and_no_fake_clock():
    p=telemetry(S,CFG['station_id'],UTC)
    assert p['timestamp']=='2026-11-14T05:00:00Z'
    assert p['measurements']['pressure_hpa'] is None
    assert p['measurements']['rain_mm'] is None
    assert p['measurements']['luminosity_pct'] is None
    assert p['measurements']['temperature_c']==23.1
    with pytest.raises(ValueError):telemetry(S,CFG['station_id'],(2000,1,1,0,0,0))

def test_invalid_sensor_missing():
    p=telemetry(SimpleNamespace(temperature=None,humidity=None),CFG['station_id'],UTC)
    assert p['quality']['temperature']=='error'
    assert p['measurements']['temperature_c'] is None

def test_config_ipv4_and_topic_guard(tmp_path):
    p=tmp_path/'cfg.json'
    assert load_config(str(p)) is None
    for invalid in ['localhost','999.0.0.1']:
        p.write_text(json.dumps(dict(CFG,enabled=True,host=invalid)))
        with pytest.raises(ValueError):load_config(str(p))
    p.write_text(json.dumps(dict(CFG,enabled=True,station_id='bad/+')))
    with pytest.raises(ValueError):load_config(str(p))
    p.write_text(json.dumps(dict(CFG,enabled=True)))
    assert load_config(str(p))['host']=='127.0.0.1'

def test_packet_encoding():
    packet=connect_frame(CFG)
    assert b'\x00\x04MQTT\x04\x02\x00\x1e' in packet
    assert frame(0x30,b'a'*128)[:3]==b'\x30\x80\x01'
    with pytest.raises(ValueError):connect_frame(dict(CFG,password='x'))

async def read_packet(reader):
    h=await reader.readexactly(1);size=0;multiple=1
    while True:
        b=(await reader.readexactly(1))[0];size+=(b&127)*multiple
        if not b&128:break
        multiple*=128
    return h[0],await reader.readexactly(size)

def test_tcp_connack_publish_and_reconnect():
    async def scenario():
        connections=[];received=[];done=asyncio.Event()
        async def broker(r,w):
            try:
                h,body=await read_packet(r);assert h==0x10
                connections.append(body)
                w.write(b'\x20\x02\x00\x00');await w.drain()
                h,body=await read_packet(r);assert h==0x30
                n=int.from_bytes(body[:2],'big');topic=body[2:2+n].decode();payload=json.loads(body[2+n:])
                received.append((topic,payload))
                if len(received)>=2:done.set()
            finally:w.close();await w.wait_closed()
        server=await asyncio.start_server(broker,'127.0.0.1',0)
        config=dict(CFG,port=server.sockets[0].getsockname()[1])
        pub=Publisher(config,lambda:True,lambda:telemetry(S,config['station_id'],UTC),lambda x:None,interval=.02,retry=.01,timeout=.1)
        task=asyncio.create_task(pub.run())
        try:
            await asyncio.wait_for(done.wait(),2)
            assert len(connections)>=2
            assert all(t=='estacao/estacao-esp32-real/telemetry' and p['measurements']['pressure_hpa'] is None for t,p in received)
        finally:
            task.cancel()
            try:await task
            except asyncio.CancelledError:pass
            server.close();await server.wait_closed()
    asyncio.run(scenario())

def test_silent_broker_does_not_block_sensor_task():
    async def scenario():
        ticks=[];clients=[]
        async def broker(r,w):
            clients.append(w)
            await r.read()
        server=await asyncio.start_server(broker,'127.0.0.1',0)
        config=dict(CFG,port=server.sockets[0].getsockname()[1])
        pub=Publisher(config,lambda:True,lambda:telemetry(S,config['station_id'],UTC),lambda x:None,retry=.01,timeout=.08)
        task=asyncio.create_task(pub.run())
        try:
            for i in range(25):ticks.append(i);await asyncio.sleep(.01)
            assert len(ticks)==25 and len(clients)>=2
        finally:
            task.cancel()
            try:await task
            except asyncio.CancelledError:pass
            for w in clients:w.close()
            server.close();await server.wait_closed()
    asyncio.run(scenario())
