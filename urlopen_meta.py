import re
import sys
import os
from urllib.request import urlopen

#마스크
#f = urlopen('http://www.welkeepsmall.com/shop/shopbrand.html?type=X&xcode=023')
#쿨패치
f = urlopen('http://www.welkeepsmall.com/shop/shopbrand.html?type=X&xcode=007')
bytes_content = f.read()

scanned_text = bytes_content[:1048576].decode('ascii',errors='replace')
match = re.search(r'charset=["\']?([\w-]+)', scanned_text)
#if match:
#    encoding = match.group(1)
#else:
#    encoding = 'utf-8'
encoding = 'cp949'
print('encoding:', encoding, file=sys.stderr)

text = bytes_content.decode(encoding)
print(text)

os.remove(r"D:\python\workspace\wellkeeps_cool_2.html")
f = open("D:\python\workspace\wellkeeps_cool_2.html", 'w')
f.write(text)
f.close()