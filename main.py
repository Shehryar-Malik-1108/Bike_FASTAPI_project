import pydantic
from bson import ObjectId
from fastapi import FastAPI
from bike_task import MyDatabase

pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str

app = FastAPI(title="Bike ki dukaan")
db = MyDatabase()


@app.get("/")
def home():
    return {"message": "Welcome to Bike ki Dukaan!!"}


@app.get("/Select_Bike")
def select_bike(id: int):
    return db.select_bike(id)


@app.post("/Insert_bike")
def insert_bike(id: int, name: str, cc: int, color: str, price: int):
    return db.insert_bike(id, name, cc, color, price)


@app.post("/Insert_many_Bikes")
def insert_many_bike(bikes):
    return db.insert_many_bike(bikes)


@app.put("/Update_bike")
def update_bike(id: int, price: int):
    return db.update_bike(id, price)


@app.put("/Update_Many_bikes")
def update_many_bikes(bikes):
    return db.update_many_bikes(bikes)


@app.delete("/Delete_bike")
def delete_bike(id: int):
    return db.delete_bike(id)
