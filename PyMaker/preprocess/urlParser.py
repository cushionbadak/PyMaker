from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import os

path = '../datas/object2/RawHTML'
file_list = os.listdir(path)    #file list in path
raw_list = []                   #dir of url texts
trash = []
trash2 = []

for i in range(len(file_list)):
    raw_list.append(path + '/' + file_list[i] + '/' + file_list[i])
    if not (os.path.isdir(path + '/' + file_list[i])):
        trash.append(path + '/' + file_list[i] + '/' + file_list[i])
        trash2.append(file_list[i])
# remove files(not dir)
for i in range(len(trash)):
    raw_list.remove(trash[i])
    file_list.remove(trash2[i])

# raw[0] has ..datas\object2\RawHTML\i1\i1 (maybe)
# file_list[i] and raw_list[i] means same thing

output_path = '../datas/object3/1st/'

for i in range(len(raw_list)):
    output_list = os.listdir(raw_list[i])
    
    for item in output_list:
        txtFile = open(raw_list[i] + '/' + item, mode = 'r', encoding = 'utf-8')
        line = txtFile.readlines()

        tmp = ''
        for j in range(len(line)):
            tmp += (line[j])[0:-1]

        if not (os.path.isdir(output_path + file_list[i])):
            os.makedirs(output_path + file_list[i])
        newFile = open(output_path + file_list[i] + '/' + item, mode = 'w', encoding = 'utf-8')

        bs = BeautifulSoup(tmp, "html.parser")
        #delete pre tag
        for pre in bs("pre"):
            pre.decompose()
        newFile.write('Natural Text\n')
        for item in bs.find_all('div', attrs= {'class':'post-text'}):
            newFile.writelines(item.text+'\n')

        newFile.write('\n\n')
        newFile.write('Answer URL\n')
        for text in bs.find_all('a', attrs={'href': re.compile("^https://docs.python.org/3/")}):
            newFile.writelines(text.get('href')+'\n')
        newFile.close()
        txtFile.close()
