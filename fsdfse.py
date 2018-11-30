import pycurl
import certifi

from io import StringIO

buffer = StringIO()
curl = pycurl.Curl()
curl.setopt(pycurl.CAINFO, "C:/Users/jepai/python-virtual-environments/env/lib/site-packages/certifi/cacert.pem")
curl.setopt(pycurl.CAINFO, certifi.where())
curl.setopt(pycurl.SSL_VERIFYPEER, 1)
curl.setopt(pycurl.SSL_VERIFYHOST, 2)
curl.setopt(curl.WRITEDATA, buffer)
curl.setopt(pycurl.URL, "https://api.twitter.com")
print(certifi.where())
body = buffer.getvalue()
print(body)
curl.perform()


