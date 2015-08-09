ipv4_w_leading_zeros_pattern = '(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)'
ipv4_wo_leading_zeros_pattern = '(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])'
ipv4_pattern = ipv4_wo_leading_zeros_pattern

import platform
def runs_on(): return platform.linux_distribution()[0]

import re
def ipv4_regex(): return re.compile('^' + ipv4_pattern + '$')

def ipv4s_regex(leading_zeros=False): 
    if leading_zeros: return re.compile(ipv4_w_leading_zeros_pattern)
    return re.compile(ipv4_wo_leading_zeros_pattern)

def ipv4_colon_port_regex():
    lastat = len(ipv4_pattern) - 1
    return '^' + ipv4_pattern[:lastat] + ':[0-9]+' + ipv4_pattern[lastat:] + '$'

def validate_ipv4s(addresses):
    for address in addresses:
        if not re.findall(ipv4_regex(), address):
            raise ValueError('The %s is not in the ipv4 format.' % address)

def validate_ipv4_colon_port(address):
    if not re.findall(ipv4_colon_port_regex(), address):
        raise ValueError('The %s is not in the ipv4:port format.' % address)

def remove_ipv4_leading_zeros(address):
    new_address = ''
    parts = address.split('.')
    for byte in parts:
        dot = ''
        lastat = len(byte) - 1
        if byte != parts[len(parts)-1]: dot = '.' 
        if len(byte) > 1:
           byte = re.sub('^0+', '', byte[:lastat]) + byte[lastat] + dot
        new_address += byte
    return new_address

def quotes_wrap(data): return "'" + str(data) + "'"

import subprocess
def start_subprocess(command, verbose):
    return subprocess.Popen(command,
        shell = verbose,
        stdout = subprocess.PIPE, 
        stderr = subprocess.STDOUT
    )

import sqlite3
def execute_sqlite3_cmd(db_path, cmd):
    connection = sqlite3.connect(db_path)
    with connection:
        cursor = connection.cursor()
        cursor.execute(cmd)
        data = cursor.fetchone()
    return data 

