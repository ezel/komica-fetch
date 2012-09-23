# filter HTML in news
# div#contents > form
# return a tuple list (id, quote, pic_id)
# the pic_id may be null

from HTMLParser import HTMLParser

full_html = ""

class MyParser(HTMLParser):
    """ Yoooooooo """
    
    @staticmethod
    def getPicIdFromTURL(url):
        basename = url.split('/')[-1]
        return basename.replace('s','',1);
        pass
    
    def reset(self):
        self.begin = False # flag , start to parser if true
        self.model = {"pos":0,"stack":[]}
        print 'reset called'
        HTMLParser.reset(self)
    
    def handle_starttag(self, tag, attrs):
        # check and set the begin flag
        if self.begin:
            if tag == 'hr':
                self.begin = False
        elif tag == "div" and ('class', 'threadpost') in attrs:
            self.begin = True
            
        # filter the date
        if self.begin:
            #print tag,attrs
            
            if tag == "img":
                for key, value in attrs:
                    if key == "src":
                        print self.getPicIdFromTURL(value)
                        break
                pass
            #print "attr %s" % [attr for attr in attrs]
        
    def handle_endtag(self, tag):
        if self.begin:
            #print "end tag %s" %tag
            pass
    def handle_data(self, data):
        if self.begin and not data.isspace():
            #print "data: %s" % data
            pass
    

def gethtml(type):
    """ Save the page in the string of full_html """
    global full_html 
    if type == 1:
        # read from a sample.html
        f = open('sample.html')
        try:
            full_html = f.read()
        finally:
            f.close()

def main():
    gethtml()
    kparser = MyParser()
    kparser.feed(full_html)
