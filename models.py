from sqlalchemy import Column, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class SwiftCode(Base):
    __tablename__ = "swift_codes"
    swift_code = Column(String, primary_key=True)
    country_iso2_code = Column(String, nullable=False)
    code_type = Column(String, nullable=False)
    bank_name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    town_name = Column(String, nullable=False)
    country_name = Column(String, nullable=False)
    time_zone = Column(String, nullable=False)
    is_headquarter = Column(Boolean, nullable=False) #to jest do wywnioskowania z kolumny swiftcode, ale wygodniej bedzie pisac zapytania, jesli bedzie tu ta kolumna

