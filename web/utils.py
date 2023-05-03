import re

REGEX_IP = re.compile(r'^fc[0-9a-f]{2}(:[0-9a-f]{4}){7}$', re.IGNORECASE)

def valid_cjdns_ip(ip):
    return REGEX_IP.match(ip) != None

def valid_cjdns_version(version):
    try:
        return int(version) < 30
    except ValueError:
        return False
