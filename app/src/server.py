import os
import re
import requests
import xmltodict
from flask import Flask
server = Flask(__name__)

@server.route("/")
 def hello():
    # limit rate to prevent DOS style attacks
   
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
