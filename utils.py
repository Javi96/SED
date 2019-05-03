# -*- coding: utf-8 -*-

import subprocess

RSA_PATH_JAVI = '/home/javi/.ssh/id_rsa.pub'
RSA_PATH_RASP = '/etc/ssh/ssh_host_ed25519_key.pub'
SAVE_FILE_PATH = '/home/pi/db/localhost.txt'
DB_PATH = '/home/pi/db'
RED_BASH = '/home/pi/red.sh'


def run_cmd(cmd):
    ip = subprocess.check_output(cmd, shell=True).decode('utf-8').replace('\n', '').split(' ')
    return ip[0]

def run_rsa(cmd):
    return subprocess.check_output(cmd, shell=True).decode('utf-8').split(' ')[1].split(':')[1]

