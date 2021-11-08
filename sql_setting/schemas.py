import datetime
from pydantic import BaseModel, Field
from typing import Optional

class WorkCreate(BaseModel):
    problem: Optional[str] = None
    scaling: Optional[str] = None
    life: Optional[str] = None
    mq: Optional[str] = None
    goal_q: Optional[str] = None

class Work(WorkCreate):
    work_id: int

    class Config:
        orm_mode = True

class PredictCreate(BaseModel):
    goal_q: Optional[str] = None
    con_01: Optional[int] = None
    con_p: Optional[float] = None
    rea_01: Optional[int] = None
    rea_p: Optional[float] = None

class Predict(PredictCreate):
    predict_id: int

    class Config:
        orm_mode = True

class GoalCreate(BaseModel):
    goal_reset: Optional[str] = None
    con_01: Optional[int] = None
    con_p: Optional[float] = None
    rea_01: Optional[int] = None
    rea_p: Optional[float] = None

class Goal(GoalCreate):
    predict_id: int

    class Config:
        orm_mode = True

