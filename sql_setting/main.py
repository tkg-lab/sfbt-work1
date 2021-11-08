from typing import List
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from transformers.utils.dummy_tf_objects import shape_list

from . import crud, models, schemas, goal_cls_fin
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
# @app.get("/")
# async def index():
#     return {"message": "Success"}

# Read
@app.get("/works", response_model=List[schemas.Work])
async def read_works(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    works = crud.get_works(db, skip=skip, limit=limit)
    return works

# Create
@app.post("/works", response_model=schemas.Work)
async def create_work(work: schemas.WorkCreate, db: Session = Depends(get_db)):
    return crud.create_work(db=db, work=work)

# Predict_get
@app.get("/predict", response_model=List[schemas.Predict])
async def read_predict(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    predicts = crud.get_predicts(db, skip=skip, limit=limit)
    return predicts

# Predict_create
@app.post("/predict", response_model=schemas.Predict)
async def create_predict(predict: schemas.PredictCreate, db: Session = Depends(get_db)):
    text = predict.goal_q
    predict = goal_cls_fin.predict(text)
    print(predict)
    return crud.create_predict(db=db, predict=predict)

# goal_reset
@app.post("/goal_reset", response_model=schemas.Goal)
async def create_goal(goal: schemas.GoalCreate, db: Session = Depends(get_db)):
    text = goal.goal_reset
    goal = goal_cls_fin.predict_2(text)
    print(goal)
    return crud.create_goal(db=db, goal=goal)

# uvicorn sql_setting.main:app --reload