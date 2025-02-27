from sqlalchemy import Column, Integer, String, JSON, DateTime, func
from app.sql_adaptor import Base

class GoogleAdsData(Base):
    __tablename__ = "google_ads_data"

    id = Column(Integer, primary_key=True, index=True)
    ads_id = Column(String, unique=True, nullable=False, index=True)
    data = Column(JSON, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
