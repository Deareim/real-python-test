import os
import re
os.system('keytool -printcert -sslserver google.com:443 >cert.txt')
fh = open("cert.txt", "r")
content = fh.readlines()
fh.close()

m = re.search('CN=(.+?),', content)
if m:
    found = m.group(1)
print(found)