import sys
sys.path.append("..")

# the unpass string warning
bad_f_n = "filter_news not pass"

stack = []

def test_fnews():
    import filter as f_n
    f = open("sample.html")
    try:
        assert f_n.full_html == ''
        stack.append("filter_news init pass")
        f_n.gethtml(1)
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
        
        f_p.formatOutput(out)
        
    except:
        raise 
    finally:
        f.close()    

def unitmain():
    
    try:
        test_fnews()
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
