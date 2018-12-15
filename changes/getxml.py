import os
import glob
import csv
from importlib import reload
import re
import io
import sys
import json
from io import StringIO
import requests
import xmltodict
reload(sys)
from lxml import etree as ET
from lxml import html

def write_to_file(xml_file):
    try:
        handle = open('file'+'.xml','w')
        handle.write(xml_file)
        return  handle
    except:
        pass
search_query='yoga'

#API URL
id_url = '''https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={}&retmode=json'''.format(search_query)
article_url='''http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&retmode=xml&id='''


print('*******************************')
print('   Getting data from server    ')
print('********************************')



#Requesting Webpages From Website URL
resp = requests.get(id_url)
if resp.status_code ==200:
    print('Got The Data :D')
else:
    print('Please Check Your Internet Connection .')
id_json=json.loads(resp.text)

#Loading Json Obtained :P ? so heavy documentaion ?
idlist = id_json['esearchresult']['idlist']



temp = ''
for id in idlist:
    temp = temp+id+','
id_data =temp.rstrip(',')

#ID String Ready :D
#Requiring Article Url
r = requests.get(article_url+id_data)
xml_file = r.text
#Saving File To Disk


xml_file= write_to_file(xml_file)

#Path For Downloaded XML FIles
path="/home/vrushang/PycharmProjects/pubmedscraper/venv/src/"

#Lets Read XML
try:
    from itertools import zip_longest as zip_longest
except:
    from itertools import izip_longest as zip_longest
dictList = []

print("***Getting the latest pubmed xml downloaded file*****")

#get the latest file with xml extension downloaded from pubmed
files_path = os.path.join(path,'*.xml')
files = sorted(
    glob.iglob(files_path), key=os.path.getctime, reverse=True
)
print("*** File is located at " + files_path)

#print the file path
xml_file = files[0]

#Parsing Part

print('***** Parsing Begins now *******')

tree = ET.parse(xml_file)
root = tree.getroot()
print(root)
print(tree)

#For Storing Afilliations
affiliation_tree = tree.xpath('//AffiliationInfo/Affiliation')
authors_tree = tree.xpath('//AuthorList/Author')
authors_list = list()
affiliation_list=list()
#IF We Have No Affiliation Skip It

if affiliation_tree is not None:
    #This Will Get Us All Text Found In Affiliation Tags In XML File
    for affil in affiliation_tree:
        affiliation_list.append(affil.text)
        #Join Complete List Seprating Them With ';!;' Delimeter
#Using Same Code To Match User Name
if authors_tree is not None:

    for a in authors_tree:

        firstname = a.find('ForeName').text if a.find('ForeName') is not None else ''
        lastname = a.find('LastName').text if a.find('LastName') is not None else ''
        fullname = (firstname + ' ' + lastname).strip()
        authors_list.append(fullname)





data = dict()
pattern = r'^[a-zA-Z0-9._-]+@+[a-zA-Z._-]+[a-zA-Z._-]*'
lcount=0
for affiliation in affiliation_list:
    lcount=lcount+1
    for items in affiliation.split(' '):
        if re.findall(pattern,items):
            data[authors_list[lcount]]=items.rstrip('.')




#name csv file as searchterm+timestamp

#Parsing XML File and appending all text together

print("***** Parsing Complete *****")

print(data)




# re_pattern = re.compile(r'[\w\.-]+@[\w\.-]+')

# with open("test.csv") as fh_in:
#     with open("mailout.csv", "a+") as fh_out:
#         for line in fh_in:
#             match_list = re_pattern.findall(line)
#             if match_list:
#                 fh_out.write(match_list[0]+"\r\n")

# #count the number of emails scrapped
# reader=csv.reader(open("mailout.csv"))
# count=0
# for row in reader:
#     count+=1
#     print "total no in row "+str(count)+" is "+str(len(row))
#     for i in row:
#         print (i)
