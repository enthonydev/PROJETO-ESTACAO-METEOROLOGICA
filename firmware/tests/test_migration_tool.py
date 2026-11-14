"""Não há acesso a USB nestes testes: todos os comandos físicos são interceptados."""
import importlib.util
import json
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('migration', ROOT/'tools/migrate_esp32.py')
migration = importlib.util.module_from_spec(spec)
spec.loader.exec_module(migration)

def test_flash_backup_failure_never_erases_board(tmp_path, monkeypatch):
    monkeypatch.setattr(migration, 'ROOT', tmp_path)
    image=tmp_path/'fw.bin'; image.write_bytes(b'firmware')
    profiles=tmp_path/'profiles.json'; profiles.write_text('[]')
    monkeypatch.setattr(migration,'get_firmware',lambda:image)
    monkeypatch.setattr(migration,'provision_profiles',lambda path:profiles)
    calls=[]
    def record(module,*args):
        calls.append((module,args))
        if 'read_flash' in args: raise OSError('porta ocupada')
    monkeypatch.setattr(migration,'run',record)
    with pytest.raises(OSError): migration.main(['--flash'])
    assert not any('erase_flash' in args or 'write_flash' in args for _,args in calls)

def test_flash_has_backup_before_erase_and_write(tmp_path, monkeypatch):
    monkeypatch.setattr(migration,'ROOT',tmp_path)
    image=tmp_path/'fw.bin'; profiles=tmp_path/'profiles.json'
    monkeypatch.setattr(migration,'get_firmware',lambda:image)
    monkeypatch.setattr(migration,'provision_profiles',lambda path:profiles)
    calls=[]
    def record(module,*args):
        calls.append((module,args))
        if 'read_flash' in args: Path(args[-1]).write_bytes(b'\0'*(4*1024*1024))
    monkeypatch.setattr(migration,'run',record)
    monkeypatch.setattr(migration,'deploy',lambda port,p:calls.append(('deploy',(port,p))))
    assert migration.main(['--flash','--port','COM7'])==0
    assert 'read_flash' in calls[0][1] and 'erase_flash' in calls[1][1]
    assert 'write_flash' in calls[2][1] and calls[-1][0]=='deploy'
    assert list((tmp_path/'backups').rglob('backup.json'))

def test_invalid_profile_does_not_reach_flash(tmp_path, monkeypatch):
    profiles=tmp_path/'profiles.json'; profiles.write_text('[{"ssid":"rede"}]')
    monkeypatch.setattr(migration,'get_firmware',lambda:tmp_path/'fw.bin')
    calls=[]; monkeypatch.setattr(migration,'run',lambda *a:calls.append(a))
    with pytest.raises(ValueError): migration.main(['--flash','--profiles',str(profiles)])
    assert calls==[]

def test_default_mode_has_no_serial_command(monkeypatch):
    calls=[]
    monkeypatch.setattr(migration,'get_firmware',lambda:Path('firmware.bin'))
    monkeypatch.setattr(migration,'run',lambda *a:calls.append(a))
    assert migration.main([])==0 and calls==[]

def test_restore_verifies_checksum_before_writing(tmp_path, monkeypatch):
    backup=tmp_path/'flash.bin'; backup.write_bytes(b'changed')
    (tmp_path/'backup.json').write_text(json.dumps({'file':'flash.bin','sha256':'wrong'}))
    calls=[]; monkeypatch.setattr(migration,'run',lambda *a:calls.append(a))
    with pytest.raises(RuntimeError): migration.main(['--restore',str(backup)])
    assert calls==[]

def test_deploy_copies_main_last_and_preserves_profile_name(tmp_path,monkeypatch):
    source=tmp_path/'firmware/src'; (source/'board').mkdir(parents=True)
    for name in ['main.py','board/station.py','board/__init__.py']:(source/name).write_text('# test')
    monkeypatch.setattr(migration,'ROOT',tmp_path)
    calls=[]; monkeypatch.setattr(migration,'run',lambda *a:calls.append(a))
    migration.deploy('COM7',tmp_path/'wifi_profiles.json')
    copies=[args for args in calls if 'cp' in args]
    assert copies[-2][-1]==':main.py' and copies[-1][-1]==':wifi_profiles.json'
    assert calls[-1][-1]=='reset'
