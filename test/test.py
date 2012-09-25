# just write easy tests which only used the built-in functions ...

import sys
sys.path.append("..")

# the unpass string warning
bad_f_n = "filter_news not pass"
bad_f_p = "filter_news not pass"
bad_m = "model not pass"

stack = []

def test_model():
    from model import model
    m = model()
    
    pos = m.__dict__["pos"]
    assert m.__dict__["pos"] == 0
    m.next();
    assert m.__dict__["pos"] == 1
    m.prev()
    assert m.__dict__["pos"] == 0
    stack.append("model init")
    
def test_fetch_page():
    validres = 633080
    validpic = "1348070226409.jpg"
    import fetch as fp
    
    assert fp.__validRid(123456) == "123456"
    assert fp.__validRid('123456') == "123456"
    assert fp.__validRid('rasd123456') == "123456"
    assert fp.__validRid('r127asd123456') == "127123"
    assert fp.__validRid('r127asd16') == False
    stack.append("fetch_page can check rid format")
    
    res = fp.__getRes(validres, fp.news)
    try:
        assert res is not None
        stack.append("fetch_page get response")
    finally:
        res.close()
    
    assert fp.__getHtml(validres, fp.news)
    stack.append("fetch_page get html")
    
    imgid = validpic
    assert ('content-type','image/jpeg') in fp.__getRes(False, fp.__getThumbUrl(imgid)).getheaders()
    assert ('content-type','image/jpeg') in fp.__getRes(False, fp.__getSrcUrl(imgid)).getheaders()
    stack.append("fetch_page get img res")
    
def test_run():
    import runner
    
def test_fnews():
    import filter_content as f_n
    f = open("sample.html")
    try:
        assert f_n.full_html == ''
        stack.append("filter_news init pass")
        
        f_n.sethtml("abcdefg1234567")
        assert f_n.full_html == "abcdefg1234567"
        stack.append("filter_news sethtml ok!")
        
        f_n.__gethtml(1)
        f.seek(0, 2)
        assert len(f_n.full_html) == f.tell()
        stack.append("filter_news gethtml")
        
        f_p = f_n.MyParser()
        out = f_p.output()
        assert f_p.model["pos"] == 0
        stack.append("filter_news model empty")
        #stack.append("%d == %d" %( len(f_p._listRes), f_p._resCount))
        
        assert len(f_p._listRes) == f_p._resCount
        stack.append("filter_news output store result")
        assert len(f_p.result) == len(f_p._listRes)
        stack.append("filter_news output generate result")
        
        #f_p.debug(out)
        
    except:
        raise 
    finally:
        f.close()    

def unitmain():
    
    try:
        test_fnews()
        #test_fetch_page()
        test_model()
        
        #test_run()
    except:
        print bad_f_n
        print "The passed: \n\t%s " % "\n\t".join(stack)
        raise
    else:
        print "All passed"
    finally:
        pass
        
if __name__ == "__main__":
    unitmain()
