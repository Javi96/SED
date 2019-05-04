# -*- coding: utf-8 -*-

import subprocess

RSA_PATH_JAVI = '/home/javi/.ssh/id_rsa.pub'
RSA_PATH_RASP = '/etc/ssh/ssh_host_ed25519_key.pub'
SAVE_FILE_PATH = './db/localhost.txt'
DB_PATH = './db'
RED_BASH = './red.sh'


def run_cmd(cmd):
    ip = subprocess.check_output(cmd, shell=True).decode('utf-8').replace('\n', '').split(' ')
    return ip[0]

def run_rsa(cmd):
    return '_'.join( subprocess.check_output(cmd, shell=True).decode('utf-8').split(' ')[:-1] )

