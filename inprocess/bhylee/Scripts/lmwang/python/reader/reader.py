from http_reqest import HTTPRequest
from simple_html_parser import SimpleHTMLParser

url = 'http://infotrac.galegroup.com/itw/infomark/0/1/1/purl=rc18_EAIM_0__jn+"Economist+(US)"?sw_aep=wash_eai'
handle=HTTPRequest.urlopen(url)
data=handle.read()
parser = SimpleHTMLParser()
parser.parse(data)

# Get the hyperlinks.
print parser.get_hyperlinks()
print parser.get_descriptions()
