
from fastapi import FastAPI, Depends, HTTPException
from database.models import Base, Users, Drug
from database.config import engine, get_db
from database.schemes import UserData, Medicine

Base.metadata.create_all(engine)


app = FastAPI()

@app.get("/")
def welcome():
    return {"message":"welcome to apteka"}

@app.post("/register/")
def register_user(user_data: UserData, db = Depends(get_db)):
    try:
      new_user = Users(**user_data.model_dump())
      db.add(new_user)
      db.commit()
      db.refresh(new_user)
      return new_user
    except Exception as error:
      return {"message":"Failed", "error":str(error)}


@app.get("/users/")
def get_users(db = Depends(get_db)):
    users = db.query(Users).all()
    return users

@app.get("/users/{user_id}")
def get_user(user_id: int, db = Depends(get_db)):
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.post("/Drugs_registor/")
def register_user(medicine: Medicine, db = Depends(get_db)):
    try:
      drug = Drug(**medicine.model_dump())
      db.add(drug)
      db.commit()
      db.refresh(drug)
      return drug
    except Exception as error:
      return {"message":"Failed", "error":str(error)}

@app.get("/Drugs/")
def print_drugs(db = Depends(get_db)):
    drugs = db.query(Drug).all()
    return drugs

@app.get("/Drugs/{drugs_name}")
def get_drugs(drugs_name: str, db = Depends(get_db)):
    user = db.query(Drug).filter(Drug.name == drugs_name).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user