import re
#import pandas as pd
from html import unescape
with open('wellkeeps_cool_2.html','r',newline='',encoding='cp949') as f:
    #f = pd.read('wellkeeps_mask.html', encoding='CP949')
    html = f.read()
#print(html)

#for partial_html in re.findall(r'<ul class="info">(.*?)</ul>', html, re.DOTALL):
#    url = re.search(r'<li class="price">', partial_html).group(1)
#    print('price:',url)
#    print('-----------')

cnt=0
for partial_html in re.findall(r'<li class="price">', html, re.DOTALL):
#for partial_html in re.findall(r'<li class="soldout">SOLD OUT</li>', html, re.DOTALL):    
    cnt=cnt+1
print('count:',cnt)
f.close()