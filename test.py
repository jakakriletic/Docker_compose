from typing import Union
from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import mysql.connector
from datetime import date
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="jaka2003",
  database="lift"
)

class Data(BaseModel):
    liftQ: str
    tezaQ: str
    repQ: str
    rpeQ: str
    sqlDateQ: date
    id_exercise: int

class nameDayInput(BaseModel):
    day_name: str

class nameLiftInput(BaseModel):
    liftName: str
    day_id: int

class nameLiftEdit(BaseModel):
    liftName: str
    day_id: int
    id: int

@app.delete("/lift/delete/{lift_id}")
async def brisi_uporabnika(lift_id: int):
    mycursor = mydb.cursor()
    sql = "delete from liftset where id = %s"
    mycursor.execute(sql, (lift_id,))
    mydb.commit()
    return "Uspešno deletano"

@app.get("/lift/izpisChart/{lift_name}") 
async def izpis_dt_lift(lift_name: str):
    mycursor = mydb.cursor()
    sql = "select teza,rep,rpe,datum from liftset where lift = %s"
    mycursor.execute(sql, (lift_name,))
    rows = mycursor.fetchall()
    array = []
    for row in rows:
        array.append({"teza": row[0],"rep": row[1],"rpe": row[2], "datum": row[3]})
    return array

@app.get("/lift/izpis/{lift_name}")
async def root(lift_name: str):
    mycursor = mydb.cursor()
    sql = "select * from liftset where lift = %s"
    mycursor.execute(sql, (lift_name,))
    rows = mycursor.fetchall()
    array = []
    for row in rows:
         array.append({"id": row[0], "lift": row[1], "teza": row[2], "rep": row[3], "rpe": row[4], "datum": row[5]})
    return array

@app.post("/lift/vpis")
async def read_root(data: Data):
    mycursor = mydb.cursor()
    sql = "INSERT INTO liftset (lift,teza, rep, rpe, datum, id_exercise) VALUES(%s, %s, %s, %s, %s, %s)"
    val = (data.liftQ,data.tezaQ, data.repQ, data.rpeQ, data.sqlDateQ,)
    mycursor.execute(sql, val)
    mydb.commit()
    return {"Rezultat": data}

@app.get("/lift/gymDay")
async def gymDay():
    mycursor = mydb.cursor()
    sql = "SELECT * from day"
    mycursor.execute(sql)
    rez = mycursor.fetchall()
    return rez

@app.post("/lift/addDay")
async def addDay(data: nameDayInput):
    mycursor = mydb.cursor()
    sql = "INSERT INTO day (day_name) VALUES(%s)"
    val = (data.day_name,)
    mycursor.execute(sql, val)
    mydb.commit()
    return "Vnos day dela"

@app.delete("/lift/deleteDay/{idDay}")
async def deleteLift(idDay: int):
    mycursor = mydb.cursor()
    sql = "DELETE FROM day where id_day = %s"
    val = (idDay,)
    mycursor.execute(sql, val)
    mydb.commit()
    return "vspešno deletano"

@app.get("/lift/getExercise/{day_id}")
async def getExercise(day_id: int):
    mycursor = mydb.cursor()
    sql = "SELECT * FROM exercise where id_day = %s"
    val = (day_id,)
    mycursor.execute(sql, val)
    rez = mycursor.fetchall()
    return rez

@app.post("/lift/addLift")
async def addLift(data: nameLiftInput):
    mycursor = mydb.cursor()
    sql = "INSERT INTO exercise (lift_name, id_day) VALUES(%s, %s)"
    val = (data.liftName, data.day_id,)
    mycursor.execute(sql, val)
    mydb.commit()
    return "Vnost lift dela"

    
@app.post("/lift/editLift")
async def addLift(data: nameLiftEdit):
    mycursor = mydb.cursor()
    sql = "update exercise SET lift_name=%s, id_day = %s where id_exercise = %s"
    val = (data.liftName, data.day_id,data.id)
    mycursor.execute(sql, val)
    mydb.commit()
    return "Edit lift končan"

@app.delete("/lift/deleteLift/{liftName}")
async def deleteLift(liftName: str):
    mycursor = mydb.cursor()
    sql = "DELETE FROM exercise where lift_name = %s"
    val = (liftName,)
    mycursor.execute(sql, val)
    mydb.commit()
    return "vspešno deletano"
    
@app.get("/lift/getProgram")
async def getProgram():
    mycursor = mydb.cursor()
    sql = "SELECT * FROM program"
    mycursor.execute(sql)
    rez = mycursor.fetchall()
    return rez