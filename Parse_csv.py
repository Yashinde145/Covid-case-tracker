# import urllib library
from urllib.request import urlopen

# import json
import json
import csv
# store the URL in url as
# parameter for urlopen
url = "https://www.mohfw.gov.in/data/datanew.json"

# store the response of URL
response = urlopen(url)

# storing the JSON response
# from url in data
data_json = json.loads(response.read())
# print the json response
print(data_json)

f_data=open(r"C:\Users\Yash\Desktop\data.csv",'w')
csvw = csv.writer(f_data)

c=0

for f in data_json:

    if c==0:
        header=f.keys()
        csvw.writerow(header)
        c+=1

    csvw.writerow(f.values())

f_data.close()