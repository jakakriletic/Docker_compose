from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector
app = FastAPI()

companies = []

class Item(BaseModel):
    company: str
    text: str

class Db(BaseModel):
    company_name: str
    ceo: str
    founded_year: int
    industry: str
    main_activity: str

def get_db_connection():
    return mysql.connector.connect(
        host="database",
        port=3306,
        user="root",
        password="123",
        database="companiesdb"
)

@app.post("/company/postdata")
def company_postdata(data: Item):
    companies.append(data)
    return companies

@app.get("/company/getdata")
def company_getdata():
    return companies

@app.post("/company/saveDb")
def save_database(data: Db):
    db = get_db_connection()
    mycursor = db.cursor()
    sql = "INSERT INTO company (company_name, ceo, founded_year, industry, main_activity) VALUES(%s, %s, %s, %s, %s)"
    val = (data.company_name, data.ceo, data.founded_year, data.industry, data.main_activity,)
    mycursor.execute(sql, val)
    db.commit()
    return {"Rezultat ": data}