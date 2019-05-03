# -*- coding: utf-8 -*-

import subprocess

RSA_PATH_JAVI = '/home/javi/.ssh/id_rsa.pub'
RSA_PATH_RASP = '/etc/ssh/ssh_host_ed25519_key.pub'


def run_cmd(cmd):
    ip = subprocess.check_output(cmd, shell=True).decode('utf-8').replace('\n', '').split(' ')
    return ip[0]

def run_rsa(cmd):
    return subprocess.check_output(cmd, shell=True).decode('utf-8').split(' ')[1].split(':')[1]

