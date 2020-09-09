import os
import re
import requests
import xmltodict
from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

server = Flask(__name__)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["1 per hour"]
)

@server.route("/")
@limiter.limit("1 per hour")
 def hello():
    # crawl webpage and filter all desired file types
    media_server = os.environ.get('MEDIA_SERVER')
    media_regex = os.environ.get('MEDIA_REGEX')
    webdav_options = """<?xml version="1.0"?>
                        <a:propfind xmlns:a="DAV:">
                        <a:prop><a:resourcetype/></a:prop>
                        </a:propfind>"""
    headers = {'Depth': 'infinity'}
    r = requests.request('PROPFIND', media_server, data=webdav_options, headers=headers)
    xml_dict = xmltodict.parse(r.text, dict_constructor=dict)

    for response in xml_dict['d:multistatus']['d:response']:
        filelink = unquote(response['d:href'])
        print(filelink)
    
    # sync with output directory
    return "Hello World!"

if __name__ == "__main__":
   server.run(host='0.0.0.0') 
