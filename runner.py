# control the main flowwork

import fetch
import filter_content
import os

# check save path
if not os.path.exists('save'):
    os.mkdir('save')
    
def save_from_fetch(*fetch_params):
    data = (fetch.img(*fetch_params))
    if data:
        img = open("./save/" + post[1], "w")
        try:
            img.write(data)
        finally:
            img.close()
    
    
if __name__ == "__main__":
    # get html page
    data = fetch.page(debug=True)
    
    print "Need download all the available image?"
    save_src = raw_input('>[n]')
    
    # get the useful data
    filter_content.sethtml(data)
    kparser = filter_content.MyParser()
    output = kparser.output()
    #kparser.debug(output)
   
    # display the result
    for post in output:
        if len(post) > 2: # have img
            #print post[1], post[2]
            # save src
            if save_src == 'y' or save_src == 'Y':
                save_from_fetch(post[1], 1)
            else:
                """ A more UX way """
                try:
                    from PIL import ImageFile
                except ImportError:
                    print "Sorry for you can't enjoy this"
                    print "You may need to install the PIL library"
                    print "use the following command:"
                    print "pip install PIL"
                else:
                    # view thumb:
                    p = ImageFile.Parser()
                    data = (fetch.img(post[1]))
                    if data:
                        p.feed(data)
                        im = p.close()
                        im.show()
                        # ask to save the source
                        print "Do you want to save the source?"
                        answer = raw_input('>')
                        if answer == 'y' or answer == 'Y': save_from_fetch(post[1], 1)
                    else:
                        p.close()
                        
