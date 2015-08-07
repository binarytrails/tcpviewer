import platform, re

ipv4_w_leading_zeros_pattern = '(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)'
ipv4_wo_leading_zeros_pattern = '(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])'
ipv4_pattern = ipv4_wo_leading_zeros_pattern

def runs_on(): return platform.linux_distribution()[0]

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

