#!/usr/bin/env python
#  -*- encoding: utf-8 -*-


def stringx_or(str1, str2):
    orxstr = ""
    for i in range(0, len(str1)):
        rst = int(str1[i]) & int(str2[i])
        orxstr = orxstr + str(rst)
    return orxstr


def bin2dec(string_num):
    return str(int(string_num, 2))


def get_ip(ip, type):
    result = ''
    for i in range(4):
        item = bin2dec(ip[0:8])
        if i == 3:
            if type == 0:
                item = str(int(item) + 1)
            else:
                item = str(int(item) - 1)
        result = result + item + '.'
        ip = ip[8:]
    return result.strip('.')


def get_cidr_start_end(cidr):
    ip = cidr.split('/')[0]
    mask = int(cidr.split('/')[1])
    ipstr = ''
    for i in ip.split('.'):
        ipstr = ipstr + bin(int(i)).replace('0b', '').zfill(8)
    pstr = '1' * mask + '0' * (32 - mask)
    res = stringx_or(ipstr, pstr)
    _ip = get_ip(res, 0), get_ip(res[0:mask] + '1' * (32 - mask), 1)
    return _ip[0] + "-" + _ip[1]


def get_all_ip_list(ip_addr):
    ip_list_tmp = []
    iptonum = lambda x: sum([256 ** j * int(i) for j, i in enumerate(x.split('.')[::-1])])
    numtoip = lambda x: '.'.join([str(x / (256 ** i) % 256) for i in range(3, -1, -1)])
    if '/' in ip_addr:
        ip_str_range = get_cidr_start_end(ip_addr)
        ip_range = ip_str_range.split('-')
        ip_start = long(iptonum(ip_range[0]))
        ip_end = long(iptonum(ip_range[1]))
        ip_count = ip_end - ip_start
        if 0 <= ip_count <= 655360:
            for ip_num in range(ip_start, ip_end + 1):
                ip_list_tmp.append(numtoip(ip_num))
        else:
            print 'IP format error'
    else:
        ip_split = ip_addr.split('.')
        net = len(ip_split)
        if net == 2:
            for b in range(1, 255):
                for c in range(1, 255):
                    ip_addr = "%s.%s.%d.%d" % (ip_split[0], ip_split[1], b, c)
                    ip_list_tmp.append(ip_addr)
        elif net == 3:
            for c in range(1, 255):
                ip_addr = "%s.%s.%s.%d" % (ip_split[0], ip_split[1], ip_split[2], c)
                ip_list_tmp.append(ip_addr)
        elif net == 4:
            ip_list_tmp.append(ip_addr)
        else:
            print "IP format error"
    return ip_list_tmp


if __name__ == '__main__':
    ip_network = "192.168.1.0/24"
    print get_all_ip_list(ip_network)
