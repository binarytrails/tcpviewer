import platform, re

ipv4_w_leading_zeros_pattern = '(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)'
ipv4_wo_leading_zeros_pattern = '(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])'

def runs_on(): return platform.linux_distribution()[0]

def ipv4_regex(): return re.compile('^' + ipv4_w_leading_zeros_pattern + '$')

def ipv4s_regex(): return re.compile(ipv4_w_leading_zeros_pattern)

def ipv4_port_regex():
    pattern = ipv4_w_leading_zeros_pattern
    last = len(pattern) - 1
    return re.compile(pattern[:last] + ':[0-9]+' + pattern[last:])

