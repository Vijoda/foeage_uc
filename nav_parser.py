import json
import urllib
from flask import Flask,request
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse,urljoin
app=Flask(__name__)

@app.route('/nav-url', methods=['POST'])
def nav_parser():
    # data=request.data
    url=request.json['url']
    data = request.json['data']
    print(url)
    soup = BeautifulSoup(data, "html.parser")
    list=[]
    list2 = []
    for tag in soup.find_all():
        if tag.name=='nav':
            for t in tag.find_all():
                if t.get('href'):
                    text_value=t.text
                    if urlparse(t.get('href')).netloc:
                        url_value=t.get('href')
                    else:
                        url_value=urljoin(url,t.get('href'))
                    list.append({'text':text_value,'url': url_value})
            for key, vaalue in enumerate(list):
                if vaalue not in list2:
                    list2.append(vaalue)
    return str(list2)

if __name__ == "__main__":
    app.run(debug=True)


