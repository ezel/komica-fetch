import sys
sys.path.append("..")

# the unpass string warning
bad_f_n = "filter_news not pass"

stack = []

def test_fnews():
    import filter_news as f_n
    f = open("sample.html")
    try:
        assert f_n.full_html == ''
        stack.append("filter_news init pass")
        f_n.gethtml(1)
        f.seek(0, 2)
        assert len(f_n.full_html) == f.tell()
        stack.append("filter_news gethtml")
        f_n.MyParser().feed(f_n.full_html)
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
