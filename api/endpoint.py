from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

companies = []

class Item(BaseModel):
    company: str
    text: str

@app.post("/company/postdata")
def company_postdata(data: Item):
    companies.append(data)
    return companies

@app.get("/company/getdata")
def company_getdata():
    return companies
