import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import os

URL = 'http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=1&brdGubun=13&ncvContSeq=&contSeq=&board_id=&gubun='
req = requests.get(URL)             #HTTP GET Request
source = req.text
soup = BeautifulSoup(source, "lxml")     #html 정보만 parsing
#print(soup)  #확인용 print
table_div = soup.find(id = "content")
tables = table_div.find_all("table")
time = table_div.find_all("div", {"class":"timetable"},"p")            # table 에서 요일정보 찾기
# print(time)
time = time[0].text
print(time)
# print(tables)

case_table = tables[0]
head = case_table.find_all(scope = 'col')
rows = case_table.find_all(scope = 'row')
numbers = case_table.find_all('td')

head2 = []
for j in range(len(head)):
    s = head[j].text
    head2.append(s)
head2 = np.array(head2)
head2 = np.delete(head2, [1])
print(head2)

rows2 =[]
for k in range(len(rows)):
    s = rows[k].text
    rows2.append(s)
rows2 = np.array(rows2)
# print(rows2)

nums = []
for i in range(len(numbers)):
    s = numbers[i].text
    nums.append(s)
nums = np.array(nums)
nums = nums.reshape(len(rows2), 8)
# print(nums)

data = pd.DataFrame(nums, columns = head2[1:], index = rows2)
# print(data)

if not os.path.exists('Corona-19_South Korea.xlsx'):
    with pd.ExcelWriter('Corona-19_South Korea.xlsx', mode = 'w', engine = 'openpyxl') as writer:
        data.to_excel(writer, sheet_name = time, startrow = 1, startcol = 1, index = True)
else:
    with pd.ExcelWriter('Corona-19_South Korea.xlsx', mode = 'a', engine='openpyxl') as writer:
        data.to_excel(writer, sheet_name = time, startrow = 1, startcol = 1, index = True)
