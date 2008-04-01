import sgmllib, re

class hrefToDictParser(sgmllib.SGMLParser):
    """A parser class process <a href=...>data</a> to python dictionary {data: href value}"""

    def parse(self, s):
        "Parse the given string 's'."
        self.feed(s)
        self.close()

    def __init__(self, verbose=0):
        "Initialise an object, passing 'verbose' to the superclass."

        sgmllib.SGMLParser.__init__(self, verbose)
        self.this_link = []
        self.this_description = []
        self.href_dict = {}
        self.text_links = []  # to store links to "Text"
        
        self.inside_a_element = 0
        self.starting_description = 0

    def start_a(self, attributes):
        "Process a hyperlink and its 'attributes'."

        for name, value in attributes:
            if name == "href":
                self.this_link = value
                self.inside_a_element = 1
                self.starting_description = 1

    def end_a(self):
        "Record the end of a hyperlink."

        self.inside_a_element = 0

    def start_img(self, attributes):
        """Process a img tag when it's inside <a> element"""

        if self.inside_a_element:
            for name, value in attributes:
                if value == "next page":
                    self.href_dict['next page'] = self.this_link

    def end_img(self):
        "Record the end of an img."

        pass

    def handle_data(self, data):
        "Handle the textual 'data'."

        if self.inside_a_element:
            if self.starting_description:
                self.this_description = data
                self.href_dict[self.this_description] = self.this_link
                if self.this_description == 'Text':
                    self.text_links.append(self.this_link)
                    
                self.starting_description = 0
            else:
                del self.href_dict[self.this_description]
                self.this_description[-1] += data
                self.href_dict[self.this_description] = self.this_link                

    def get_href_dict(self):
        "Return the href_dict"

        return self.href_dict

    def get_text_links(self):
        """return self.text_links"""

        return self.text_links

    def find_exact_match_url(self, find_str):
        """return the value in dictionary self.href_dict whose key matches find_str"""
        for k, v in self.href_dict.items():
            if find_str == k:
                return v

        return None

    def find_match_url(self, find_str):
        """return the first value in dictionary self.href_dict whose key matches find_str"""
        for k, v in self.href_dict.items():
            if re.search(find_str, k):
                return v
        return None
