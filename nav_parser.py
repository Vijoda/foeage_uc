import json
import urllib
from flask import Flask,request
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse,urljoin
app=Flask(__name__)

def domain_find(input_url):
    input_url = re.sub('.*//', '', input_url)
    input_url = re.sub('.*//', '', input_url)
    if '/' in input_url:
        input_url = re.sub('/.*', '', input_url)
    input_url = re.sub("www.|ww3.", "", input_url)
    return input_url

@app.route('/nav-url', methods=['POST'])
def nav_parser():
    url=request.json['url']
    data = request.json['data']
    domain=None
    site_name=None
    site_flag=None
    copyright_site=None
    right_site=None
    domain=domain_find(url)
    soup = BeautifulSoup(data, "html.parser")
    list=[]
    list2 = []

    for tag in soup.find_all():
        if tag.name=='meta' and 'og:site_name' in str(tag):
            # print(tag)
            site_name=tag.get('content')
            site_flag='meta'
        if '©' in tag.text or 'copyright' in tag.text or 'Copyright' in tag.text:
            copyright = tag.text
            copyright = re.sub(r"[\n\t]*", "", copyright)
            copyright = copyright.strip()
            if len(copyright)>2 and len(copyright)<70:
                # print(copyright)
                copyright_site=copyright

        if 'All rights reserved' in tag.text or 'All Rights Reserved' in tag.text:
            right = tag.text
            right = re.sub(r"[\n\t]*", "", right)
            right = right.strip()
            if len(right) > 2 and len(right) < 70:
                right_site=right

        if tag.name=='nav' or tag.name=='ul':
            for t in tag.find_all():
                if t.get('href'):
                    text_value=t.text
                    text_value = re.sub(r"[\n\t]*", "", text_value)
                    text_value = text_value.strip()
                    if urlparse(t.get('href')).netloc:
                        url_value=t.get('href')
                        if 'http' not in str(url_value):
                            url_value=None
                    else:
                        url_value=urljoin(url,t.get('href'))
                        if 'http' not in str(url_value):
                            url_value=None
                    if  url_value!=None:
                        list.append({'text':text_value,'url': url_value})
    if site_name==None:
        if copyright_site!=None:
            site_name =copyright_site
            site_flag = 'copyright'
        elif right_site !=None:
            site_name=right_site
            site_flag='right reserved'
    for key, value in enumerate(list):
        value['domain'] = domain
        value['flag'] = site_flag
        value['site_name'] = site_name
        if value not in list2:
            list2.append(value)
    return str(list2)

if __name__ == "__main__":
    app.run(debug=True)


