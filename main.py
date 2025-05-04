from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from collections import OrderedDict
from models import SwiftCode, Base

app = FastAPI()
engine = create_engine("sqlite:///swift_codes.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

# pojedynczy SWIFT code (dla centrali lub oddziału)
class SwiftCodeBranchResponse(BaseModel):
    address: str
    bankName: str
    countryISO2: str
    isHeadquarter: bool
    swiftCode: str

class SwiftCodeResponse(SwiftCodeBranchResponse):
    countryName: Optional[str] = None

# odpowiedź dla kraju
class CountryResponse(BaseModel):
    countryISO2: str
    countryName: str
    swiftCodes: List[SwiftCodeBranchResponse]

# struktura danych wejściowych dla POST
class SwiftCodeCreateRequest(BaseModel):
    address: str
    bankName: str
    countryISO2: str
    countryName: str
    isHeadquarter: bool = Field(..., alias="isHeadquarter")
    swiftCode: str

    model_config = ConfigDict(populate_by_name=True)

@app.get("/v1/swift-codes/{swift_code}", response_model=None, response_class=JSONResponse)
def get_swift_code(swift_code: str):
    session = Session()
    code = session.query(SwiftCode).filter_by(swift_code=swift_code).first()

    if not code:
        session.close()
        raise HTTPException(status_code=404, detail="SWIFT code not found")

    full_address = f"{code.address}, {code.town_name}"

    if code.is_headquarter:
        branches = session.query(SwiftCode).filter(
            SwiftCode.swift_code.startswith(code.swift_code[:8]),
            SwiftCode.swift_code != code.swift_code
        ).all()

        response = OrderedDict([
            ("address", full_address),
            ("bankName", code.bank_name),
            ("countryISO2", code.country_iso2_code),
            ("countryName", code.country_name),
            ("isHeadquarter", True),
            ("swiftCode", code.swift_code),
            ("branches", [
                OrderedDict([
                    ("address", f"{b.address}, {b.town_name}"),
                    ("bankName", b.bank_name),
                    ("countryISO2", b.country_iso2_code),
                    ("isHeadquarter", b.is_headquarter),
                    ("swiftCode", b.swift_code)
                ]) for b in branches
            ])
        ])
    else:
        response = OrderedDict([
            ("address", full_address),
            ("bankName", code.bank_name),
            ("countryISO2", code.country_iso2_code),
            ("countryName", code.country_name),
            ("isHeadquarter", False),
            ("swiftCode", code.swift_code)
        ])

    session.close()
    return JSONResponse(content=response)

@app.get("/v1/swift-codes/country/{countryISO2code}", response_model=None, response_class=JSONResponse)
def get_swift_codes_by_country(countryISO2code: str):
    session = Session()
    records = session.query(SwiftCode).filter_by(country_iso2_code=countryISO2code.upper()).all()

    if not records:
        session.close()
        raise HTTPException(status_code=404, detail="No SWIFT code for the country")

    swift_codes = [
        OrderedDict([
            ("address", f"{r.address}, {r.town_name}"),
            ("bankName", r.bank_name),
            ("countryISO2", r.country_iso2_code),
            ("isHeadquarter", r.is_headquarter),
            ("swiftCode", r.swift_code)
        ]) for r in records
    ]

    response = OrderedDict([
        ("countryISO2", records[0].country_iso2_code),
        ("countryName", records[0].country_name),
        ("swiftCodes", swift_codes)
    ])

    session.close()
    return JSONResponse(content=response)

@app.post("/v1/swift-codes")
def add_swift_code(data: SwiftCodeCreateRequest):
    session = Session()
    exists = session.query(SwiftCode).filter_by(swift_code=data.swiftCode).first()

    if exists:
        session.close()
        raise HTTPException(status_code=400, detail="SWIFT code already exists")

    new_entry = SwiftCode(
        swift_code=data.swiftCode,
        bank_name=data.bankName,
        address=data.address,
        town_name="",
        country_iso2_code=data.countryISO2.upper(),
        country_name=data.countryName.upper(),
        code_type="BIC11",
        time_zone="UTC",
        is_headquarter=data.isHeadquarter
    )

    session.add(new_entry)
    session.commit()
    session.close()
    return {"message": "SWIFT code added successfully"}

@app.delete("/v1/swift-codes/{swift_code}")
def delete_swift_code(swift_code: str):
    session = Session()
    record = session.query(SwiftCode).filter_by(swift_code=swift_code).first()

    if not record:
        session.close()
        raise HTTPException(status_code=404, detail="SWIFT code does not exist")

    session.delete(record)
    session.commit()
    session.close()
    return {"message": "SWIFT code deleted successfully"}
