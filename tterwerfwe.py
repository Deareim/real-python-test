import requests
import ssl


print(requests.get('https://www.howsmyssl.com/a/check', verify="C:/Users/jepai/python-virtual-environments/cacert.pem").json()['tls_version'])


