# -*- coding: utf-8 -*-

# set page info and fetch page from komica
# will return a full html 
# page url example for news board:
#     http://2cat.or.tl/~tedc21thc/new/pixmicat.php?res=628153

# TODO: add #qXXXXXX search in threadlist

hostname = "2cat.or.tl"
news = "~tedc21thc/new/pixmicat.php"
names = ["news", "live"]
nameszh = ["新番捏他", "新番實況"]
paths = [news, "~tedc21thc/live/index.php"]
boardpaths = ["~tedc21thc/new/", "~tedc21thc/live/"]

import os
import httplib, urllib

def imenu():
    """
    An easy interface, used to 
    1. select news/live
    2. input res id
    TODO: add unit test for raw_input
    """
    str_select = ["Choose the board name:"]
    str_select.extend(["%i.%s(%s) " % (i, nameszh[i], names[i]) for i in range(len(names))])
    str_select.append("Enter the number of board ...")
    str_select[1] = str_select[1] + "[default]"
    str_rid = "\nPlease enter the res id: (e.g. 633080)"
    
    # get board name
    print "\n".join(str_select)
    select = raw_input('>[0]')
    if select not in range(len(paths)):
        select = 0
    print "You choosed %s(%s)" % (nameszh[select], names[select])
    
    # get res id
    rid = False
    while not rid:
        print str_rid
        rid = __validRid(raw_input('>'))
        
    return rid,paths[select]
    
def __validRid(raw, board=0):
    # TODO: check rid valid from komica
    # filter the first 6 nums
    raw = str(raw)
    if len(raw) < 6:
        return False
    
    rid = []
    for i in raw:
        if i.isdigit():
            rid.append(i)
        if len(rid) == 6:
            break
        
    if len(rid) != 6:
        return False
    
    return "".join(rid)

def __getRes(rid, path):
    conn = httplib.HTTPConnection(hostname, timeout=20)
    
    if rid:
        params = urllib.urlencode({'res': rid})
        conn.request("GET", "%s?%s" %( path, params))
    else:
        conn.request("GET", path)

    return conn.getresponse()

def __getHtml(rid, path=None):
    res = __getRes(rid, path)
    if res.status == 200:
        return res.read()

    return ''

def page(debug=False):
    if debug:
        return __getHtml(rid=633080, path=paths[0])
    rid, path = imenu()
    return __getHtml(rid, path)

def img(pid, type=0, board=0):
    """
    Type 0 => thumb, 1 => src
    Board 0 => news, 1 => None
    """
    # TODO: need a check func
    func = [__getThumbUrl, __getSrcUrl]
    path = func[type](pid)
    res = __getRes(False, path)
    print "%s: %s" %(pid, res.status)
    if res.status != 200:
        return False
    return res.read()

def __getSrcUrl(pic, board=0):
    prefix = boardpaths[board] + "src/"
    return prefix + pic

def __getThumbUrl(pic, board=0):
    prefix = boardpaths[board] + "thumb/"
    tmpl = pic.split('.')
    return "%s%ss.%s" % (prefix, tmpl[0], tmpl[1])
