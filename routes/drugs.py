from fastapi import APIRouter, Depends, HTTPException
from database.config import get_db
from database.models import Drug, Users
from database.schemes import DrugData, DrugDataUpdate

drug_route = APIRouter(tags=["Drug routelari"])

def is_admin(user_id:int, db = Depends(get_db)):
    user = db.query(Users).get(user_id)

    if user is None or user.role.value != "admin":
        raise HTTPException(status_code=401, detail="Not found")


@drug_route.post("/drug-create/")
def drug_create(drug_data: DrugData, admin_id: int, db = Depends(get_db)):
    admin_user = db.query(Users).filter(Users.id == admin_id).first()

    if admin_user.role.value == "admin":
        new_drug = Drug(**drug_data.model_dump())
        db.add(new_drug)
        db.commit()

        new_drug.bar_code = f"{new_drug.id}-{new_drug.name}"
        db.commit()
        db.refresh(new_drug)

        return {"message":"Created ! ", "success":True, "data":new_drug}

    else:
        return {"message":"Bir aylanib kelish !", "success":False}



@drug_route.get("/get_drugs/{drugs_id}")
def get_drugs(drug_id: int, user_id:int,  db = Depends(get_db)):
    user = db.query(Users).get(user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    drug = db.query(Drug).get(drug_id)

    if drug is None:
        raise HTTPException(status_code=404, detail="Not found")
    

    return {"Message": "worked", "success":True, "data":drug}


@drug_route.put("/drug_update/")
def update_drug(admin_id: int, drug_data: DrugDataUpdate, db = Depends(get_db)):
    admin_user = db.query(Users).get(admin_id)

    if admin_user.role.value != "admin" or admin_user is None:
        raise HTTPException(status_code=404, detail="Not found")

    drug = db.query(Drug).get(drug_data.id)

    if drug is None:
        raise HTTPException(status_code=404, detail="Not found")
    new_data = drug_data.model_dump(exclude_unset=True)

    for key, value in new_data.items():
        setattr(drug, key, value)

    db.commit()
    db.refresh(drug)

    return {"Message":"Updated", "success":True, "data":drug}



@drug_route.delete("/delete_drug/{drug_id}")
def delete_drug(admin_id: int,drug_id: int, db = Depends(get_db)):
    admin_user = db.query(Users).filter(Users.id == admin_id).first()
    if admin_user.role.value == "admin":
        drug_del = db.query(Drug).filter(Drug.id == drug_id).first()
        db.delete(Drug)
        db.commit()
        return {"message": "drug delete", "success":True}
    else:
        return {"message": "Bir aylanib keling", "success":False}

@drug_route.get("/all-drugs/")
def all_drugs(admin_id: int, db = Depends(get_db)):
    admin_user = db.query(Users).filter(Users.id == admin_id).first()

    if admin_user.role.value == "admin":
        drugs = db.query(Drug).all()
        return {"message":"Fetched successfully !", "success":True, "data":drugs}
    else:
        return {"message": "Bir aylanib keling", "success":False}