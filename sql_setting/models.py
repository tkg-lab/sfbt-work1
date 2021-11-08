from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.sql.sqltypes import Float
from .database import Base

# SQLAlchemyのデータ構造を指定

class Work(Base):
    __tablename__ = 'works'
    work_id = Column(Integer, primary_key=True, index=True, nullable=False)
    problem = Column(String, index=True)
    scaling = Column(String, index=True)
    life = Column(String, index=True)
    mq = Column(String, index=True)
    goal_q = Column(String, index=True)

class Predict(Base):
    __tablename__ = 'predicts'
    predict_id = Column(Integer, primary_key=True, index=True, nullable=False)
    goal_q = Column(String, index=True)
    con_01 = Column(Integer, index=True)
    con_p = Column(Float, index=True)
    rea_01 = Column(Integer, index=True)
    rea_p = Column(Float, index=True)

class Goal(Base):
    __tablename__ = 'goals'
    predict_id = Column(Integer, primary_key=True, index=True, nullable=False)
    goal_reset = Column(String, index=True)
    con_01 = Column(Integer, index=True)
    con_p = Column(Float, index=True)
    rea_01 = Column(Integer, index=True)
    rea_p = Column(Float, index=True)