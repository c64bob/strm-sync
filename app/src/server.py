import os
import re
import requests
import xmltodict
from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

server = Flask(__name__)
limiter = Limiter(
    server,
    key_func=get_remote_address,
    default_limits=["1 per hour"]
)

@server.route("/health")
@limiter.limit("1 per second")
def health():
    return "ok"
    
@server.route("/")
@limiter.limit("1 per hour")
def hello():
    # crawl webpage and filter all desired file types
    media_server = os.environ.get('MEDIA_SERVER')
    media_regex = os.environ.get('MEDIA_REGEX')
    filelinks = []
    outdir = "/media"
    webdav_options = """<?xml version="1.0"?>
                        <a:propfind xmlns:a="DAV:">
                        <a:prop><a:resourcetype/></a:prop>
                        </a:propfind>"""
    headers = {'Depth': 'infinity'}
    r = requests.request('PROPFIND', media_server, data=webdav_options, headers=headers)
    xml_dict = xmltodict.parse(r.text, dict_constructor=dict)
    
    for response in xml_dict['D:multistatus']['D:response']:
        filelink = requests.utils.unquote(response['D:href'])
        match = re.search(media_regex, filelink, re.IGNORECASE)
        if match:
            filelinks.append(filelink)

    # sync with output directory
    # Todo: delete files in outdir that no longer exist on the media server
    for filelink in filelinks:
        # parse folder structure
        match = re.match("^/Movies/([^/]+)$", filelink)
        if match:
            filename = match.group(1) + ".strm"
            fulllink = media_server + filelink
            writefile = True
            if not os.path.isdir(os.path.join(outdir, "Movies")):
                os.mkdir(os.path.join(outdir, "Movies"))
            if os.path.isfile(os.path.join(outdir, "Movies", filename)):
                with open(os.path.join(outdir, "Movies", filename)) as f:
                    if f.read() == fulllink:
                        writefile = False
            if writefile:
                with open(os.path.join(outdir, "Movies", filename), "w") as f:
                    f.write(fulllink)

        match = re.match("^/TVShows/([^/]+)/([^/]+)$", filelink)
        if match:
            foldername = match.group(1)
            filename = match.group(2) + ".strm"
            fulllink = media_server + filelink
            writefile = True
            if not os.path.isdir(os.path.join(outdir, "TVShows")):
                os.mkdir(os.path.join(outdir, "TVShows"))
            if not os.path.isdir(os.path.join(outdir, "TVShows", foldername)):
                os.mkdir(os.path.join(outdir, "TVShows", foldername))
            if os.path.isfile(os.path.join(outdir, "TVShows", foldername, filename)):
                with open(os.path.join(outdir, "TVShows", foldername, filename)) as f:
                    if f.read() == fulllink:
                        writefile = False
            if writefile:
                with open(os.path.join(outdir, "TVShows", foldername, filename), "w") as f:
                    f.write(fulllink)

    # trigger a library rescan
    if os.environ.get('MEDIA_API_KEY') and os.environ.get('MEDIA_API_URL'):
        headers = {'X-MediaBrowser-Token': os.environ.get('MEDIA_API_KEY')}
        r = requests.post(os.environ.get('MEDIA_API_URL'), headers=headers)

    # finished
    return "finished syncing strm files"

if __name__ == "__main__":
   server.run(host='0.0.0.0') 
