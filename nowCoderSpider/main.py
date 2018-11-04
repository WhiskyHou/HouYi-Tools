# encoding = utf-8

import requests
import lxml
import re
from bs4 import BeautifulSoup

url1 = "https://www.nowcoder.com/profile/"
url2 = "/codeBooks?q=&onlyAcc=0&page="

user_id = [831479610, 284825274]
array = {"831479610": {}, "284825274": {}}

for id in user_id:
    page_id = 1
    while 1:
        request = requests.get(url=url1+str(id)+url2+str(page_id))
        if request.status_code == 200:
            soup = BeautifulSoup(request.text, 'lxml')
            labels = soup.find_all("tr")
            if labels.__len__() == 1:
                break
            for i in range(1, labels.__len__()):
                soup_temp = BeautifulSoup(str(labels[i]), 'lxml')
                name = soup_temp.find("a").text
                tds = soup_temp.find_all("td")
                time = tds[3].text
                memory = tds[4].text
                language = tds[5].text
                name = re.sub('[\n]', '', name)
                time = re.sub('[\n]', ' ', time)
                solution = {"time": time, "memory": memory, "language": language}
                array[str(id)].update({str(name): solution})
        page_id += 1

print("题目".rjust(12, " ") + "C++".rjust(20, " ") + "Python".rjust(20, " "))
for obj in array['831479610']:
    print('{:<{len}}'.format(str(obj), len=22 - len(str(obj).encode('GBK')) + len(obj)), end="")
    # if len(obj) > 13:
    #     print("\t", end="")
    # elif len(obj) > 9:
    #     print("\t\t", end="")
    # elif len(obj) > 5:
    #     print("\t\t\t", end="")
    print("\t", end="")
    print(str(array['831479610'][obj]['time']).rjust(6, " ") + "\t" +
          str(array['831479610'][obj]['memory']).rjust(6, " ") + "\t" +
          str(array['284825274'][obj]['time']).rjust(8, " ") + "\t" +
          str(array['284825274'][obj]['memory']).rjust(6, " "))
