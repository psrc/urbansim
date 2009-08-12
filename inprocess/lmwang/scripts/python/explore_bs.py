import urllib

usock = urllib.urlopen('http://www.blogger.com/redirect/next_blog.pyra?navBar=true')
htmlSource = usock.read()
usock.close()
print htmlSource
