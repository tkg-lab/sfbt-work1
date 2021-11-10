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
    def __repr__(self):
        return "<Work(work_id = %s, problem = '%s', scaling = '%s', life = '%s', mq = '%s', goal_q = '%s')>" % (self.work_id, self.problem, self.scaling, self.life, self.mq, self.goal_q)

class Predict(Base):
    __tablename__ = 'predicts'
    predict_id = Column(Integer, primary_key=True, index=True, nullable=False)
    goal_q = Column(String, index=True)
    con_01 = Column(Integer, index=True)
    con_p = Column(Float, index=True)
    rea_01 = Column(Integer, index=True)
    rea_p = Column(Float, index=True)
    def __repr__(self):
        return "<Predict(predict_id = %s, goal_q = '%s', con_01 = '%s', con_p = '%s', rea_01 = '%s', rea_p = '%s')>" % (self.predict_id, self.goal_q, self.con_01, self.con_p, self.rea_01, self.rea_p)


class Goal(Base):
    __tablename__ = 'goals'
    predict_id = Column(Integer, primary_key=True, index=True, nullable=False)
    goal_reset = Column(String, index=True)
    con_01 = Column(Integer, index=True)
    con_p = Column(Float, index=True)
    rea_01 = Column(Integer, index=True)
    rea_p = Column(Float, index=True)
    def __repr__(self):
        return "<Predict(predict_id = %s, goal_reset = '%s', con_01 = '%s', con_p = '%s', rea_01 = '%s', rea_p = '%s')>" % (self.predict_id, self.goal_reset, self.con_01, self.con_p, self.rea_01, self.rea_p)
