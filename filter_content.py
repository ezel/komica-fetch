# filter HTML in news
# div#contents > form

# TODO override the self.model to a class

from HTMLParser import HTMLParser

full_html = ""

def getSrcUrl(pic):
    prefix = "http://2cat.or.tl/~tedc21thc/new/src/"
    return prefix + pic

def getThumbUrl(pic):
    prefix = "http://2cat.or.tl/~tedc21thc/new/thumb/"
    tmpl = pic.split('.')
    return "%s%ss.%s" % (prefix, tmpl[0], tmpl[1])
    

class MyParser(HTMLParser):
    """ 
    The class will parser a full_html string into a tuple list,
    like (id, pic_id, quote)     # pic_id may be None
    use output method to generate the tuple list
    """
    
    @staticmethod
    def getPicIdFromTURL(url):
        basename = url.split('/')[-1]
        return basename.replace('s','',1);
    
    @staticmethod
    def formatOutput(result):
        for i in range(len(result)):
            print i
            for j in range(len(result[i])):
                print "%d:%s" % (j,result[i][j])
    
    def reset(self):
        # the stacklist save the (pushCon, handleTag, popCon, handleData) functions
        # the return value of pushCon/popCon can be set to a number
        self.model = {"pos":0,"stack":[]}
        
        # save the tuple (id, quote, pic_id) in result 
        # the pic_id may be null
        self.result = []
        self._listRes = []
        self._eachRes =[]
        self._eachDate = []
        self._resCount = 0
        
        # set up the callback?
        self.model["stack"].append(
            #(lambda *parg: parg[0] == "div" and ('id', 'contents') in parg[1], None, lambda *parg: False, None))
            (lambda *parg: parg[0] == "div" and ('class', 'threadpost') in parg[1], None, lambda *parg: False, None))
        
        self.model["stack"].append(
            (lambda *parg: parg[0] == "img" and 1 or ( (parg[0]=="div" and ('class','quote') in parg[1]) and 2),
             lambda *parg: [v for k,v in parg[1] if k == "id" and ( ('class', 'threadpost') in parg[1] or ('class', 'reply') in parg[1])], 
             lambda *parg: parg[0] == "hr",
             None))
        
        self.model["stack"].append(
            (lambda *parg: False,
             lambda *parg: apply(self.getPicIdFromTURL, [v for k, v in parg[1] if k=="src"]),
             lambda *parg: parg[0] == "img",
             None))
        
        self.model["stack"].append(
            (lambda *parg: False,
             None,
             lambda *parg: parg[0] == "div" and 2,
             lambda *parg: parg))
        
        # print 'reset called'
        HTMLParser.reset(self)
    
    def handle_starttag(self, tag, attrs):
        # push stack
        check = self.model["stack"][self.model["pos"]][0](tag, attrs)
        if check:
            if type(check) == type(1):
                self.model["pos"] += check
            else:
                self.model["pos"] += 1
            
        handle = self.model["stack"][self.model["pos"]][1]
        if handle is not None:
            val = handle(tag, attrs)
            if len(val):
                if type(val) == type([]):
                    if self._eachRes:
                        if self._eachDate:
                            self._eachRes.append("".join(self._eachDate))
                        self._listRes.append(self._eachRes)
                        self._resCount += 1
                    self._eachRes = val
                    self._eachDate = []
                elif type(val) == type('str'):
                    self._eachRes.append(val)
                    #print "append %s to _list" % self._eachRes
        
    def handle_endtag(self, tag):
        # pop stack
        check = self.model["stack"][self.model["pos"]][2](tag)
        if check:
            #print "WRYYYYY %s" %tag
            if type(check) == type(1):
                self.model["pos"] -= check
            else:
                self.model["pos"] -= 1
                
    def handle_data(self, data):
        handle = self.model["stack"][self.model["pos"]][3]
        if handle is not None:
            val = handle(data)
            if len(val):
                """
                if self._eachDate:
                    self._eachDate.append("\n")
                """
                self._eachDate.append(val[0])
            
    def output(self):
        self.feed(full_html)
        # update the result if need
        if len(self.result) != self._resCount:
            self.result = [tuple(l) for l in self._listRes]
        return self.result

def __gethtml(type):
    """ Save the page in the string of full_html """
    global full_html 
    if type == 1:
        # read from a sample.html
        f = open('sample.html')
        try:
            full_html = f.read()
        finally:
            f.close()
            
def sethtml(str):
    global full_html
    full_html = str

"""
the main flow:

def main(data):
    # gethtml() or sethtml
    sethtml(data)
    kparser = MyParser()
    return kparser.output()
"""
