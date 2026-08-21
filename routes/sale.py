from fastapi import APIRouter, Depends, HTTPException
from database.config import get_db
from database.models import Users, Check, CheckItem, Drug
from database.schemes import Check, CheckItems

check_sale = APIRouter(tags=["Kassa Checks"])

@check_sale.post("/drug-create/")
def drug_create(cashier_is:Check, db = Depends(get_db)):

    new_check = Check(**cashier_is.model_dump())
    db.add(new_check)
    db.commit()
    db.refresh(new_check)

    return {"message":"Created ! ", "success":True, "data":new_check}