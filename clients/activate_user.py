#!/usr/bin/env python3

import json
import argparse

from urllib.request import Request, urlopen
from urllib.parse import urlencode

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('losturl', type=str)
    parser.add_argument('username', type=str)
    parser.add_argument('password', type=str)
    parser.add_argument('role', type=str)
    args = parser.parse_args()
    losturl = args.losturl

    data = dict()
    data['username'] = args.username
    data['password'] = args.password
    data['role'] = args.role

    json_data = dict()
    json_data['arguments'] = json.dumps(data)
    json_data['signature'] = ''
    send_data = urlencode(json_data)
    
    post_request = Request(losturl, send_data.encode('ascii'), method='POST')
