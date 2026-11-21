"""Instalação local explícita do ESP32, com backup da flash antes de apagar."""
from __future__ import annotations

import argparse
from datetime import datetime
from getpass import getpass
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
FIRMWARE_NAME = 'ESP32_GENERIC-20250911-v1.26.1.bin'
FIRMWARE_URL = 'https://micropython.org/resources/firmware/' + FIRMWARE_NAME


def run(module, *args):
    subprocess.run([sys.executable, '-m', module, *map(str, args)], check=True)


def get_firmware():
    path = ROOT / 'firmware-images' / FIRMWARE_NAME
    path.parent.mkdir(exist_ok=True)
    expected = json.loads((ROOT / 'firmware' / 'release.json').read_text())['sha256']
    if not path.exists():
        temporary = path.with_suffix('.download')
        with urlopen(FIRMWARE_URL, timeout=45) as response, temporary.open('wb') as target:
            while block := response.read(65536):
                target.write(block)
        temporary.replace(path)
    if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
        raise RuntimeError('Arquivo MicroPython difere do SHA-256 do pacote. Não será gravado.')
    return path


def provision_profiles(path):
    path = Path(path)
    if path.exists():
        profiles = json.loads(path.read_text(encoding='utf-8'))
    else:
        profiles = []
        print('Configure suas redes aqui no notebook. Senhas não aparecem no terminal.')
        while True:
            ssid = input('Nome da rede 2,4 GHz (Enter para terminar): ').strip()
            if not ssid:
                break
            profiles.append({'ssid': ssid, 'password': getpass('Senha (vazio somente se rede aberta): ')})
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(profiles, ensure_ascii=False, indent=2), encoding='utf-8')
    if not isinstance(profiles, list) or any(
        not isinstance(p, dict) or not isinstance(p.get('ssid'), str) or not p['ssid']
        or not isinstance(p.get('password'), str) for p in profiles
    ):
        raise ValueError('Perfis Wi-Fi inválidos. Corrija o arquivo local antes de gravar.')
    return path


def backup_flash(port):
    folder = ROOT / 'backups' / datetime.now().strftime('%Y%m%d-%H%M%S')
    folder.mkdir(parents=True, exist_ok=False)
    path = folder / 'flash-antes-micropython.bin'
    run('esptool', '--chip', 'esp32', '--port', port, '--baud', '115200',
        'read_flash', '0', 'ALL', path)
    size = path.stat().st_size
    if size < 4 * 1024 * 1024:
        raise RuntimeError('Backup inferior a 4 MiB. Pare: verifique variante e capacidade da placa.')
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    (folder / 'backup.json').write_text(json.dumps({
        'port': port, 'bytes': size, 'sha256': digest, 'file': path.name,
    }, indent=2), encoding='utf-8')
    print('Backup da flash salvo em:', path)
    return path


def deploy(port, profiles):
    source = ROOT / 'firmware' / 'src'
    # Cria diretórios explicitamente e transfere o main.py por último.
    directories = sorted({str(p.parent.relative_to(source)).replace('\\', '/')
                          for p in source.rglob('*.py') if p.parent != source})
    for directory in directories:
        code = 'import os\ntry:\n os.mkdir(%r)\nexcept OSError as e:\n if e.args[0] != 17: raise\n' % directory
        run('mpremote', 'connect', port, 'exec', code)
    files = sorted(source.rglob('*.py'), key=lambda p: (p.name == 'main.py', str(p)))
    for path in files:
        target = ':' + str(path.relative_to(source)).replace('\\', '/')
        run('mpremote', 'connect', port, 'fs', 'cp', path, target)
    run('mpremote', 'connect', port, 'fs', 'cp', profiles, ':wifi_profiles.json')
    run('mpremote', 'connect', port, 'reset')
    print('Arquivos enviados. Abra Thonny/terminal em 115200 e observe OLED e logs.')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', default='COM7')
    parser.add_argument('--profiles', type=Path, default=ROOT / 'wifi_profiles.json')
    parser.add_argument('--flash', action='store_true', help='Backup + apagar + gravar MicroPython + enviar app')
    parser.add_argument('--deploy', action='store_true', help='Atualizar arquivos em placa que já possui MicroPython')
    parser.add_argument('--restore', type=Path, help='Restaurar backup integral da MESMA placa')
    args = parser.parse_args(argv)
    if sum((args.flash, args.deploy, args.restore is not None)) > 1:
        parser.error('Escolha somente --flash, --deploy ou --restore.')
    if args.restore is not None:
        backup = args.restore.resolve()
        metadata = json.loads((backup.parent / 'backup.json').read_text())
        if backup.name != metadata['file'] or hashlib.sha256(backup.read_bytes()).hexdigest() != metadata['sha256']:
            raise RuntimeError('Backup não passou na verificação; restauração cancelada.')
        run('esptool', '--chip', 'esp32', '--port', args.port, '--baud', '115200', 'write_flash', '0', backup)
        return 0
    if not (args.flash or args.deploy):
        get_firmware()
        print('Pacote verificado. Nenhuma porta serial foi aberta ou flash alterada.')
        print('Para migrar: python tools/migrate_esp32.py --port COM7 --flash')
        return 0
    image = get_firmware()  # Validação antes de qualquer escrita na placa.
    profiles = provision_profiles(args.profiles)
    if args.flash:
        backup_flash(args.port)  # Falha aqui impede a etapa de apagar.
        run('esptool', '--chip', 'esp32', '--port', args.port, 'erase_flash')
        run('esptool', '--chip', 'esp32', '--port', args.port, '--baud', '115200',
            'write_flash', '0x1000', image)
    deploy(args.port, profiles)
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (OSError, ValueError, RuntimeError, subprocess.CalledProcessError) as error:
        print('Migração interrompida:', error, file=sys.stderr)
        print('Não apague o backup. Feche outros monitores seriais e confira a porta.', file=sys.stderr)
        raise SystemExit(1)
