from sqlalchemy.orm import Session

import sql_setting.models as models
import sql_setting.schemas as schemas

# 回答一覧を取得する
def get_works(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Work).offset(skip).limit(limit).all()

# 回答の登録
def create_work(db: Session, work: schemas.Work):
    db_work = models.Work(
        problem = work['problem'],
        scaling = work['scaling'],
        life = work['life'],
        mq = work['mq'],
        goal_q = work['goal_q']
        )
    db.add(db_work)
    db.commit()
    db.refresh(db_work)
    return db_work

# 予測値の取得
def get_predicts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Predict).offset(skip).limit(limit).all()

# 予測値の作成
def create_predict(db: Session, predict: schemas.Predict):
    db_predict = models.Predict(
        goal_q = predict["goal_q"],
        con_01 = predict["con_01"],
        con_p = predict["con_p"],
        rea_01 = predict["rea_01"],
        rea_p = predict["rea_p"]
        )
    db.add(db_predict)
    db.commit()
    db.refresh(db_predict)
    return db_predict


def get_goal(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Goal).offset(skip).limit(limit).all()

def create_goal(db: Session, goal: schemas.Goal):
    db_goal = models.Goal(
        goal_reset = goal["goal_reset"],
        con_01 = goal["con_01"],
        con_p = goal["con_p"],
        rea_01 = goal["rea_01"],
        rea_p = goal["rea_p"]
        )
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    return db_goal
