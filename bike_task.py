import pymongo


class MyDatabase:
    def __int__(self):
        pass

    def get_db(self, db_name="mydb"):
        client = pymongo.MongoClient(f"mongodb://127.0.0.1:27017/{db_name}")
        if db_name not in client.list_database_names():
            print(f"Database '{db_name}' not found, creating...")
            db = client[db_name]

            db.create_collection("bikes")

        db = client.get_database(db_name)

        print(f"Returning DB: {db_name}")
        return db

    def select_bike(self, id: int):
        db = self.get_db()
        col = db.get_collection("bikes")
        bike1 = col.find_one({"id": id})
        return bike1

    def insert_bike(self, id: int, name: str, cc: int, color: str, price: int, bikes=None):
        db = self.get_db()
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

    def insert_many_bike(self, bikes):
        db = self.get_db()
        col = db.get_collection("bikes")
        new_bikes = col.insert_many([bike.dict() for bike in bikes])
        if new_bikes.acknowledged:
            return {"message": f"{len(new_bikes.inserted_ids)} bikes created"}
        return {"message": "Error occurred while creating new bike(s)."}

    def update_bike(self, id: int, price: int):
        db = self.get_db()
        col = db.get_collection("bikes")
        bike_dict = {k: v for k, v in {"price": price}.items() if v is not None}
        result = col.update_one({"id": id}, {"$set": bike_dict})
        if result.modified_count == 1:
            return {"message": f"Bike updated."}
        return {"message": f"Error occurred while updating bike."}

    def update_many_bikes(self, bikes):
        db = self.get_db()
        col = db.get_collection("bikes")
        result = col.update_many(
            {"id": {"$in": [b.id for b in bikes]}},
            {"$set": {k: v for b in bikes for k, v in b.dict(exclude={"id"}).items() if v is not None}}
        )
        if result.modified_count > 0:
            return {"message": f"{result.modified_count} bike(s) updated."}
        return {"message": "No bikes updated."}

    def delete_bike(self, id: int):
        db = self.get_db()
        col = db.get_collection("bikes")
        result = col.delete_one({"id": id})
        if result.deleted_count == 1:
            return {"message": "Bikes deleted"}
        return {"message": "error occurred while deleting bikes."}


if __name__ == "__main__":
    pass
