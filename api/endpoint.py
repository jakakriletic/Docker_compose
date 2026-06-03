from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

companies = []

class Item(BaseModel):
    Company: str
    Ceo: str = None
    Creation_date: str = "00/00/2000"

@app.post("/company/postdata")
def company_postdata(data: Item):
    companies.append(data)
    return companies

@app.get("/company/getdata")
def company_getdata():
    return companies
