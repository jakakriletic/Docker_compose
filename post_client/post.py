import httpx
import json


with open("companies.json","r" , encoding="utf-8") as file:
    companies = json.load(file)

for company in companies:
    r = httpx.post("http://api:80/company/postdata", json=company)



  

