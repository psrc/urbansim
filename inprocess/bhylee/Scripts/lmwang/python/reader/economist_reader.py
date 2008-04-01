from http_request import HTTPRequest
from simple_html_parser import SimpleHTMLParser
from href_to_dict_parser import hrefToDictParser
import re

# handle=HTTPRequest().urlopen(url)
# data=handle.read()
# parser = SimpleHTMLParser()
# parser.parse(data)

# # Get the hyperlinks.
# print parser.get_hyperlinks()
# print parser.get_descriptions()

class EconomistReader:
    entry_url = 'http://infotrac.galegroup.com/itw/infomark/0/1/1/purl=rc18_EAIM_0__jn+"Economist+(US)"?sw_aep=wash_eai'
    def __init__(self):
        self.hostname = 'http://infotrac.galegroup.com'
        self.request = HTTPRequest()
        self.parser = hrefToDictParser()
        self.data = self.get_html_data(self.entry_url)
        self.parser.parse(self.data)
        
    def get_html_data(self, url):
        hd = self.request.urlopen(url)
        return hd.read()

    def get_year_page(self, year):
        year_url = self.parser.find_exact_match_url(year)
        year_url = self.hostname+year_url
        if year_url is None:  #search year 2006 at the entry page, do nothing since current page is the page for 2006
            #year_url = "http://infotrac.galegroup.com/itw/infomark/733/332/83414510w2/purl=rc19_EAIM_0__Economist+(US)_%s&dyn=3!jn_d_Economist+(US)_%s?sw_aep=wash_eai" % (year, year)
            year_url = self.entry_url
        self.data=self.get_html_data(year_url)
        self.parser.parse(self.data)
        #return self.parse.get_href_dict()

    def get_issue_pages(self, issue):
        """issue number"""
        text_links = []
        issue_url = self.parser.find_match_url(issue)
        if issue_url is not None:
            self.data=self.get_html_data(self.hostname+issue_url)
            self.parser.parse(self.data)
            text_links += self.parser.get_text_links()
            next_page_link = self.parser.find_match_url('next page')
            next_page_link = self._replace_js_bmkUrl(next_page_link)
#             while next_page_link:
#                 import pdb; pdb.set_trace()
#                 self.data=self.get_html_data(self.hostname+next_page_link)
#                 del self.parser.href_dict['next page']   #empty href_dict next page
#                 self.parser.parse(self.data)
#                 text_links += self.parser.get_text_links()
#                 next_page_link = self.parser.find_match_url('next page')
#                 next_page_link = self._replace_js_bmkUrl(next_page_link)

        text_links = self._replace_js_bmkUrl(text_links)
        return text_links

    def get_article_pdf(self, article_link, pdf_file_name):
        self.data = self.get_html_data(article_link)
        self.parser.parse(self.data)
        pdf_link = self.hostname+self.parser.find_match_url('Acrobat Reader')
        pdf_data = self.get_html_data(pdf_link)
        fd = open(pdf_file_name, 'w')
        fd.write(pdf_data)
        
        
    def _replace_js_bmkUrl(self, links):
        expanded_links = []
        if not isinstance(links, list):
            links = [links]
        for link in links:
            p = re.compile("javascript:bkmUrl\('(.*)','(.*)'\)")
            m = p.match(link)
            expanded_links.append("/itw/infomark/172/292/82203275w4" + m.group(1) + "?sw_aep=wash_eai" + m.group(2))

        if len(expanded_links) == 1:
            return expanded_links[0]
        else:
            return expanded_links
            
    

    
