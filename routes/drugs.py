from fastapi import APIRouter, Depends
from database.config import get_db
from database.models import Drug, Users
from database.schemes import DrugData, Drugupdata

drug_route = APIRouter(tags=["Drug routelari"])

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

@drug_route.get("/all-drugs/")
def all_drugs(admin_id: int, db = Depends(get_db)):
    admin_user = db.query(Users).filter(Users.id == admin_id).first()

    if admin_user.role.value == "admin":
        users = db.query(Drug).all()
        return {"message":"Fetched successfully !", "success":True, "data":users}
    else:
        return {"message": "Bir aylanib keling", "success":False}

@drug_route.get("/get_drugs/{drugs_name}")
def get_drugs(drug_name: str,admin_id: int, db = Depends(get_db)):
    admin_user = db.query(Users).filter(Users.id == admin_id).first()

    if admin_user.role.value == "admin":
        drug = db.query(Drug).filter(Drug.name == drug_name).first()
        return drug
    else:
        return {"message": "Bir aylanib keling", "success":False}

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

@drug_route.put("/update_drug/")
def update_drug(admin_id: int, drug_data: Drugupdata, db = Depends(get_db)):
    admin_user = db.query(Users).filter(Users.id == admin_id).first()
    if admin_user.role.value == "admin":
        drug = db.query(Drug).filter(Drug.id == drug_data.id).first()

        new_drug_data = drug_data.model_dump(exclud e_unset=True)

        for key, value in new_drug_data.items():
            setattr(drug, key, value)
            db.commit()
            db.refresh(drug)
            return {"message":"Updated !", "success":True, "data":drug}
    else:
        return{"message":"Bir aylanib keling", "seccess":False}
