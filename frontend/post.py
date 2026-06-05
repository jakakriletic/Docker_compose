import httpx
import json


def start_app():
    with open("companies.json","r" , encoding="utf-8") as file:
        companies = json.load(file)

    for company in companies:
        r = httpx.post("http://api:80/company/postdata", json=company)


input("1 za nadeljevanje")

if input == 1:
    start_app()
  

