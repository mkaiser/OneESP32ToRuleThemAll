"""Retake the TTF07 C dashboard screenshots into docs/images/ttf07c/ (run on the HA host, e.g. the SSH add-on).

    python3 .claude/tools/dashboard/take_screenshots.py

Steps: create a temporary local-only admin user with a random password (HA websocket API through the
Supervisor proxy), run screenshots_playwright.py in the Playwright container (docker create / cp / start,
because the Docker daemon resolves bind mounts on the host OS, not in this add-on), copy the PNGs out,
delete the container and the user (also on failure). Details: .wiki/wiki/screenshots.md.
"""
import os, sys, secrets, subprocess
sys.path.insert(0, '/homeassistant/.claude/tools/naming')  # ws(): HA websocket helper of the HA config repo
from ha import ws
HERE = os.path.dirname(os.path.abspath(__file__))
DST = os.path.join(HERE, '..', '..', '..', 'docs', 'images', 'ttf07c') + '/'
IMAGE = 'mcr.microsoft.com/playwright/python:v1.49.1-noble'
def run(*a, **k):
    p = subprocess.run(list(a), capture_output=True, text=True, **k)
    print(a[1], p.returncode, p.stdout[-1500:], p.stderr[-800:] if p.returncode else '')
user, pw = 'screenshots-tmp', secrets.token_urlsafe(24)
r = ws([{'type': 'config/auth/create', 'name': 'Screenshots (temporary)', 'group_ids': ['system-admin'], 'local_only': True}])[0]
assert r['success'], r
uid = r['result']['user']['id']; name = 'ha-screenshots-tmp'
try:
    assert ws([{'type': 'config/auth_provider/homeassistant/create', 'user_id': uid, 'username': user, 'password': pw}])[0]['success']
    run('docker', 'create', '--name', name, '--network', 'host', '--ipc', 'host', '-e', 'HA_USER=' + user, '-e', 'HA_PASS=' + pw,
        IMAGE, 'bash', '-c',
        'mkdir -p /out && pip install -q --root-user-action=ignore --default-timeout=120 --retries 5 playwright==1.49.1; python3 -I /ha_screenshots.py')
    run('docker', 'cp', os.path.join(HERE, 'screenshots_playwright.py'), name + ':/ha_screenshots.py')
    run('docker', 'start', '-a', name, timeout=600)
    run('docker', 'cp', name + ':/out/.', DST)
finally:
    subprocess.run(['docker', 'rm', '-f', name], capture_output=True)
    print('temp user deleted:', ws([{'type': 'config/auth/delete', 'user_id': uid}])[0]['success'])
