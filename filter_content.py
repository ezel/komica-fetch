# filter HTML in news
# div#contents > form

from HTMLParser import HTMLParser

def setup():
    import model
    models =[] 
    tmpM = model.model()
    # funcs: (nextCond, prevCond, handleTag, handleData)
    tmpM.push(
        lambda *parg: parg[0] == "div" and ('class', 'threadpost') in parg[1], None, None, None)
    
    tmpM.push(
        lambda *parg: parg[0] == "img" and 1 or ( (parg[0]=="div" and ('class','quote') in parg[1]) and 2),
        lambda *parg: parg[0] == "hr",
        lambda *parg: [v for k,v in parg[1] if k == "id" and ( ('class', 'threadpost') in parg[1] or ('class', 'reply') in parg[1])], 
        None)
    
    tmpM.push(
        None,
        lambda *parg: parg[0] == "img",
        lambda *parg: apply(MyParser.getPicIdFromTURL, [v for k, v in parg[1] if k=="src"]),
        None)
    
    tmpM.push(
        None,
        lambda *parg: parg[0] == "div" and 2,
        None,
        lambda *parg: parg)
    
    models.append(tmpM)
    
    return models

full_html = ""
models = setup()

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
    def debug(result):
        for i in range(len(result)):
            print "%d: len %d" %(i, len(result[i]))
            for j in range(len(result[i])):
                print "%d:%s" % (j,result[i][j])
    
    def __init__(self, modelval=models[0]):
        self.model = models[0]
        
        # save the tuple (id, quote, pic_id) in result 
        # the pic_id may be null
        self.result = []
        self._listRes = []
        self._eachRes =[]
        self._eachDate = []
        self._resCount = 0
       
        HTMLParser.__init__(self)
    
    def handle_starttag(self, tag, attrs):
        # push stack
        self.model.next(tag, attrs)
            
        handle = self.model.getHandleTag()
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
        
    def handle_endtag(self, tag):
        # pop stack
        self.model.prev(tag)
                
    def handle_data(self, data):
        handle = self.model.getHandleData()
        if handle is not None:
            val = handle(data)
            if len(val):
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

