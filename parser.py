import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import SwiftCode, Base

def load_data(file_path: str, url = "sqlite:///swift_codes.db"):
    df = pd.read_excel(file_path) #trzeba doinstalowac openpyxl

    df = df.rename(columns={
        "SWIFT CODE": "swift_code",
        "NAME": "bank_name",
        "ADDRESS": "address",
        "TOWN NAME": "town_name",
        "COUNTRY ISO2 CODE": "country_iso2_code",
        "COUNTRY NAME": "country_name",
        "CODE TYPE": "code_type",
        "TIME ZONE": "time_zone"
    })

    #wystanaryzowanie country_iso2_code i country_name na duże litery + dodanie kolumny is_headquarter
    df["country_iso2_code"] = df["country_iso2_code"].str.upper()
    df["country_name"] = df["country_name"].str.upper()
    df["is_headquarter"] = df["swift_code"].str.endswith("XXX")

    print(df)

    engine = create_engine(url)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind = engine)
    session = Session()

    for _, row in df.iterrows():
        entry = SwiftCode(
            swift_code=row["swift_code"],
            bank_name=row["bank_name"],
            address=row["address"],
            town_name=row["town_name"],
            country_iso2_code=row["country_iso2_code"],
            country_name=row["country_name"],
            code_type=row["code_type"],
            time_zone=row["time_zone"],
            is_headquarter=row["is_headquarter"]
        )
        session.merge(entry)

    session.commit()
    session.close()

load_data("Interns_2025_SWIFT_CODES.xlsx","sqlite:///swift_codes.db")