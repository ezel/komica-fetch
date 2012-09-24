# set page info
# and fetch page from komica
# return a full html 
# like http://2cat.or.tl/~tedc21thc/new/pixmicat.php?res=628153

# TODO add #qXXXXXX search in threadlist

hostname = "2cat.or.tl"
news = "~tedc21thc/new/pixmicat.php"
live = "~tedc21thc/live/index.php"

import os
import httplib, urllib

def imenu():
    """
    an easy interface, used to 
    1. select news/live
    2. input res id
    """
    # TODO check rid valid
    # add unit test for default val
    
    pass

def __getRes(rid, path):
    params = urllib.urlencode({'res': rid})

    conn = httplib.HTTPConnection(hostname, timeout=20)
    conn.request("GET", "%s?%s" %( path, params))

    return conn.getresponse()

def __getHtml(rid, path=None):
    path = news
    res = __getRes(rid, path)
    if res.status == 200:
        return res.read()

    return ''

def page():
    #rid, path = imenu()
    rid = 633080
    path = news
    return __getHtml(rid, path)

def img(url):
    pass
