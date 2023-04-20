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


@app.get("/All_Bikes")
def get_all_bikes():
    return db.get_all_bikes()


@app.post("/Insert_bike")
def insert_bike(id: int, name: str, cc: int, color: str, price: int):
    return db.insert_bike(id, name, cc, color, price)


@app.post("/Insert_many_bikes")
def insert_many_bike(bikes: list):
    return db.insert_many_bike(bikes)


@app.put("/Update_bike")
def update_bike(id: int, price: int):
    return db.update_bike(id, price)


@app.put("/Update_many_bikes")
def update_many_bikes(bikes: list[dict]):
    return db.update_many_bikes(bikes)


@app.delete("/Delete_bike")
def delete_bike(id: int):
    return db.delete_bike(id)


@app.delete("/Delete_many_bikes")
def delete_many_bikes(bikes: list[int]):
    return db.delete_many_bikes(bikes)
