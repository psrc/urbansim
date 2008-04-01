
COOKIEFILE = 'cookies.lwp'
import urllib2, os
import cookielib #for python2.4 only use ClientCookie for 2.3

class HTTPRequest:
    def __init__(self):
        cj = cookielib.LWPCookieJar()
        if cj != None:
            if os.path.isfile(COOKIEFILE):
                cj.load(COOKIEFILE)
            if cookielib:
                opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
                urllib2.install_opener(opener)

        self.url_open = urllib2.urlopen
        self.Request=urllib2.Request
        
    def urlopen(self, url):
        #theurl = 'http://infotrac.galegroup.com/itw/infomark/0/1/1/purl=rc18_EAIM_0__jn+"Economist+(US)"?sw_aep=wash_eai'
        txdata = None
        txheaders =  {'User-agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}

        try:
            req = self.Request(url, txdata, txheaders)            # create a request object
            handle = self.url_open(req)                               # and open it to return a handle on the url
        except IOError, e:
            print 'failed to open "%s".' % url
            if hasattr(e, 'code'):
                print 'failed with error code - %s.' % e.code

        return handle
    
# print
# if cj == None:
#     print "We don't have a cookie library available - sorry."
#     print "I can't show you any cookies."
# else:
#     print 'These are the cookies we have received so far :'
#     for index, cookie in enumerate(cj):
#         print index, '  :  ', cookie        
#     cj.save(COOKIEFILE)                     # save the cookies again


