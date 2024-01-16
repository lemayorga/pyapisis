from sqlalchemy import Column, String, Boolean, Integer
from infra.database.setting_db import Base

class Catalogue (Base):
    __tablename__ = 'catalogue'
    __table_args__ = {"schema":"commun"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    group = Column(String, nullable=False)
    value = Column(String, nullable=False)
    description = Column(String, nullable=True)
    is_active = Column('is_active', Boolean, nullable=False, default=True)