import os
import scrapy
from flask import Flask
server = Flask(__name__)

@server.route("/")
 def hello():
    # limit rate to prevent DOS style attacks
   
    # crawl webpage and filter all desired file types
    media_server = os.environ.get('MEDIA_SERVER')
    #if media_server:
     
    
    # sync with output directory
    return "Hello World!"

if __name__ == "__main__":
   server.run(host='0.0.0.0') 
