# control the main flowwork

# get the html
import fetch

data = fetch.main()

# get the useful content
import filter_content

filter_content.sethtml(data)
kparser = filter_content.MyParser()
output = kparser.output()

# display the result
kparser.formatOutput(output)
