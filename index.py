#!/usr/bin/python3
from bs4 import BeautifulSoup
from urllib import parse
import requests, json#, re
import time
import sys

#Id = parse.quote(input("Youtube video id: ")) # Like: 9iHM6X6uUH8
#Id = sys.argv[1]
Id ='uVjRe8QXFHY'

res = requests.post("https://www.y2mate.com/mates/en115/analyze/ajax",
                  headers={
                      "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                      "X-Requested-With": "XMLHttpRequest",
                      "Alt-Used": "www.y2mate.com",
                      "Sec-Fetch-Dest": "empty",
                      "Sec-Fetch-Mode": "cors",
                      "Sec-Fetch-Site": "same-origin"
                      },
                  # data="url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3D{}&q_auto=0&ajax=1".format(Id)
                  )
data = json.loads(res.content)
if not data['status'] == 'success':
    raise RuntimeError(f"data['status'] == {data['status']}")
soup = BeautifulSoup(data['result'], "html.parser")
if not soup.findChild().attrs['class'] == ['tabs', 'row']:
    raise FileNotFoundError("Video does not exist")
name = soup.find('div', {'class': ['caption', 'text-left']}).findChild('b').getText()
#print(name)
myScript = soup.find('script', {'type':'text/javascript'}).getText()
#print('DEBUG:', myScript)
#getId = re.compile(r'(?<=var k__id = ")\w*(?=";)')
tmpID = myScript[70+len(name):70+24+len(name)] #re.findall(getId, myScript)[0]
#print('DEBUG:', tmpID, '(<- need to bee the value of var k__id)')
links = soup.findAll('a', {'class': ["btn", "btn-success"]})
streams = []
for i, link in enumerate(links):
    stream = {
        'quality': link.attrs['data-fquality'],
        'type': link.attrs['data-ftype']
        }
    streams.append(stream)
    print(f'{i+1}: {stream}')

#myStream = streams[int(input(f"Select stream [1-{len(streams)}]: "))-1]
myStream = streams[0]


res = requests.post("https://www.y2mate.com/mates/convert",
                    headers={
                        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                        "X-Requested-With": "XMLHttpRequest",
                        "Alt-Used": "www.y2mate.com",
                        "Sec-Fetch-Dest": "empty",
                        "Sec-Fetch-Mode": "cors",
                        "Sec-Fetch-Site": "same-origin"
                        },
                    data="type=youtube&_id={verify}&v_id={vid}&ajax=1&token=&ftype={type}&fquality={quality}" \
                        .format(**myStream, verify=tmpID, vid=Id)
                    )
                    

data = json.loads(res.content)
#print(data)

if not data['status'] == 'success':
    raise RuntimeError(f"data['status'] == {data['status']}")
    

    
soup = BeautifulSoup(data['result'], "html.parser")
download = soup.find('a', {'class': ['btn', 'btn-success', 'btn-file']})
toDownload = download.attrs['href']

#print('Here is the download link:')
print(toDownload)
