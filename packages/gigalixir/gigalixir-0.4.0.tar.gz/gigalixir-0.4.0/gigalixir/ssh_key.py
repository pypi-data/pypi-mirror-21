import requests
from . import auth
import json
import click

def get(host):
    r = requests.get('%s/api/ssh_keys' % host, headers = {
        'Content-Type': 'application/json',
    })
    if r.status_code != 200:
        if r.status_code == 401:
            raise auth.AuthException()
        raise Exception(r.text)
    else:
        data = json.loads(r.text)["data"]
        click.echo(json.dumps(data, indent=2, sort_keys=True))

def create(host, key):
    r = requests.post('%s/api/ssh_keys' % host, headers = {
        'Content-Type': 'application/json',
    }, json = {
        "ssh_key": key,
    })
    if r.status_code != 201:
        if r.status_code == 401:
            raise auth.AuthException()
        raise Exception(r.text)

def delete(host, key_id):
    r = requests.delete('%s/api/ssh_keys/%s' % (host, key_id), headers = {
        'Content-Type': 'application/json',
    })
    if r.status_code != 200:
        if r.status_code == 401:
            raise auth.AuthException()
        raise Exception(r.text)
