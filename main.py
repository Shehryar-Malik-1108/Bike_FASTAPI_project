from fastapi import FastAPI
import pymongo
import os
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI(title="Bike ki dukaan")


@app.get("/")
def home():
    return {"message": "Welcome to Bike ki Dukaan!!"}


class Bikes(BaseModel):
    id: int
    name: str
    cc: int
    color: str
    price: int


class BikeUpdates(BaseModel):
    id: int
    name: Optional[str] = None
    cc: int
    color: Optional[str] = None
    price: int


def get_db(db_name="mydb"):
    client = pymongo.MongoClient(os.getenv("MONGO_URL"))
    db = client.get_database(db_name)
    if db_name not in client.list_database_names():
        print(f"Database '{db_name}' not found, creating...")
        db = client[db_name]

        db.create_collection("bikes")
    return db


@app.get("/Select_Bike", response_model=Bikes)
def select_bike(id: int):
    db = get_db()
    col = db.get_collection("bikes")
    bike = col.find_one({"id": id})
    return bike


@app.get("/Get_All_Records", response_model=List[Bikes])
def get_all_bikes():
    db = get_db()
    col = db.get_collection("bikes")
    bikes = col.find()
    return [Bikes(**bike) for bike in bikes]


@app.post("/Insert_bike")
def create_bike(id: int, name: str, cc: int, color: str, price: int, bikes: Optional[List[Bikes]] = None):
    db = get_db()
    col = db.get_collection("bikes")

    if bikes is None:

        new_bike = col.insert_one({"id": id, "name": name, "cc": cc, "color": color, "price": price})
        if new_bike.acknowledged:
            return {"message": f"Bike {name} created"}
    else:

        new_bikes = col.insert_many([bike.dict() for bike in bikes])
        if new_bikes.acknowledged:
            return {"message": f"{len(new_bikes.inserted_ids)} bikes created"}

    return {"message": "Error occurred while creating new bike(s)."}


@app.post("/Insert_many_Bikes")
def insert_many_bike(bikes: List[Bikes]):
    db = get_db()
    col = db.get_collection("bikes")
    new_bikes = col.insert_many([bike.dict() for bike in bikes])
    if new_bikes.acknowledged:
        return {"message": f"{len(new_bikes.inserted_ids)} bikes created"}
    return {"message": "Error occurred while creating new bike(s)."}


@app.put("/Update_bike")
def update_bike(id: int, color: Optional[str] = None, price: Optional[int] = None):
    db = get_db()
    col = db.get_collection("bikes")
    bike_dict = {k: v for k, v in {"color": color, "price": price}.items() if v is not None}
    result = col.update_one({"id": id}, {"$set": bike_dict})
    if result.modified_count == 1:
        return {"message": f"Bike updated."}
    return {"message": f"Error occurred while updating bike."}


@app.put("/Update_Many_bikes")
def update_many_bikes(bikes: List[BikeUpdates]):
    db = get_db()
    col = db.get_collection("bikes")
    result = col.update_many(
        {"id": {"$in": [b.id for b in bikes]}},
        {"$set": {k: v for b in bikes for k, v in b.dict(exclude={"id"}).items() if v is not None}}
    )
    if result.modified_count > 0:
        return {"message": f"{result.modified_count} bike(s) updated."}
    return {"message": "No bikes updated."}


@app.delete("/Delete_bike")
def delete_bike(id: int):
    db = get_db()
    col = db.get_collection("Bikes")
    result = col.delete_one({"id": id})
    if result.deleted_count == 1:
        return {"message": "Bikes deleted"}
    return {"message": "error occurred while deleting bikes."}


bike = Bikes(id=1, name="CD70", cc=70, color="Black", price=15000)