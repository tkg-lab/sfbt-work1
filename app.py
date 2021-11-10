import streamlit as st
import pandas as pd

from sqlalchemy.orm import Session, sessionmaker
from transformers.utils.dummy_tf_objects import shape_list

import sql_setting.models as models
import sql_setting.crud as crud
from sql_setting.database import SessionLocal, engine
import sql_setting.goal_cls_fin as goal_cls_fin

models.Base.metadata.create_all(bind=engine)
SessionClass = sessionmaker(engine)  # セッションを作るクラスを作成
session = SessionClass()

page = 'works'

if page == 'works':
    st.title('目標焦点型のワーク')
    with st.form(key='work'):
        st.write('あなたの生活に対して、継続して否定的な影響を与えている問題を一つ教えてください。  \nここで書くうえで、支障が無い程度の問題で構いません。4W1H(いつ、誰が、誰に、何を、どのように、どのくらいの期間)を意識して、できるだけ具体的に問題を教えてください。')
        problem: str = st.text_input('Q1')
        st.write('----')
        st.write('上でお答えいただいた問題がとても深刻で最も悪い状態を0点とします。  \nそして、問題があっても何とか自分自身の力でやっていける状態を10点とします。  \n現在、あなたにとってその問題は、何点ぐらいだと思いますか？  \nいずれかの数字を選んでください。')
        scaling: int = st.selectbox(label='Q2', options=('',0,1,2,3,4,5,6,7,8,9,10))
        st.write('生活全般について、とても深刻で最も悪い状態を0点とします。  \nそして、とても理想的な生活を送れている状態を10点とします。  \n現在のあなたの生活は何点ぐらいだと思いますか？  \nいずれかの数字を選んでください。')
        life: int = st.selectbox(label='Q3', options=('',0,1,2,3,4,5,6,7,8,9,10))
        st.write('----')
        st.write('もしも奇跡が起きて、上で書いた問題が全くなくなったら、どんな一日を過ごすでしょうか。  \n「朝から昼まで」、「昼から夕方まで」、「夕方から夜まで」の時間帯で、今の生活と何が変わるか思いつくことをすべて、箇条書きで書きましょう。  \n＊想像力を膨らませて、自由に考えてみましょう。  \n＊大きな変化がないと感じる場合は、小さな変化を教えてください。')
        mq: str = st.text_input('Q4')
        st.write('----')
        st.write('上で書いたような生活を送るために、必要な目標を箇条書きで書きましょう。なお、目標は次の条件に当てはまるように設定してください。  \n■ できるだけ具体的な、目で確認できるような行動レベルの目標  \n■ できるだけ小さくて、現実的な目標（最終的な目標ではなく、最初の小さな兆し）  \n■ 「～しない」という否定的な目標ではなく、「～する」という肯定的な目標  \n＊「～しない」という目標を思いついた場合は、それをしなくなる代わりに何をするようになるのかを考えてみましょう')
        goal_q: str = st.text_input('Q5')
        data = {
            'problem': problem,
            'scaling': scaling,
            'life': life,
            'mq': mq,
            'goal_q': goal_q
        }

        if 'push1' not in st.session_state: # ここを追加
            st.session_state.push1 = False #push1がsession_stateに追加されていない場合，False

        submit_button = st.form_submit_button(label='目標の具体性と現実性を判定する')

        if submit_button: # ここを追加
            st.session_state.push1 = True #button1が押下された場合，Trueを保持

        if st.session_state.push1:
            # st.json(data)
            works = crud.create_work(db=session, work=data)
            st.warning('目標の解析中です。判定結果が出るまで少しお待ちください ( . . . )')

            # st.write(works)
            df_works = pd.DataFrame(data,index=['your answer',])
            df_works.columns = ['problem', 'scaling', 'life', 'mq', 'goal_q']
            # st.table(df_works)

            # 予測の処理
            text = works.goal_q
            predict = goal_cls_fin.predict(text)
            # st.write(predict)
            crud.create_predict(db=session, predict=predict)

            # 予測値の表示
            # st.write(predict)
            df_predicts = pd.DataFrame(predict,index=['予測結果',])
            df_predicts.columns = ['goal_q', 'con_01', 'con_p', 'rea_01', 'rea_p']
            # st.table(df_predicts)
            st.success('解析が終わりました。判定結果をご確認ください。')
            con_p = df_predicts.iat[0, 2]
            con_p = '{:.02f}'.format(con_p*100)
            rea_p = df_predicts.iat[0, 4]
            rea_p = '{:.02f}'.format(rea_p*100)
            st.subheader(f'あなたが設定した目標は「{df_predicts.iat[0,0]}」です')
            st.subheader(f'この目標が、具体的である確率は{con_p}%です。')
            st.subheader(f'この目標が、現実的である確率は{rea_p}%です。')

            st.write('----')
            st.header('目標の再設定')
            st.write('具体性が高まるように目標を修正してみましょう。コツは、時間帯、場所、具体的な行動を設定することです。もしも、気持ちに関する目標を設定した場合は、そのような気持ちになったら何をするようになるかをお答えください。「～までに」という期日を設定することも効果的です。  \nもし「～しない」という目標を設定した場合は、その代わりに何をするのかをお答えください。')
            goal_reset: str = st.text_input('Q6', value=goal_q)
            data2 = {
                'goal_reset': goal_reset
            }

            resubmit_button = st.form_submit_button(label='再設定した目標の具体性と現実性を判定する')
            st.write('* 何回でも判定することができます。納得がいくまで目標を修正してみてください。')

            if resubmit_button:
                # st.json(data)
                st.warning('目標の解析中です。判定結果が出るまで少しお待ちください ( . . . )')
                text = goal_reset
                predict2 = goal_cls_fin.predict_2(text)
                # st.write(predict)
                crud.create_goal(db=session, goal=predict2)

                # 予測値の表示
                # st.write(predict)
                df_predicts2 = pd.DataFrame(predict2,index=['予測結果',])
                df_predicts2.columns = ['goal_reset', 'con_01', 'con_p', 'rea_01', 'rea_p']
                # st.table(df_predicts)
                st.success('解析が終わりました。判定結果をご確認ください。')
                con_p = df_predicts2.iat[0, 2]
                con_p = '{:.02f}'.format(con_p*100)
                rea_p = df_predicts2.iat[0, 4]
                rea_p = '{:.02f}'.format(rea_p*100)
                st.subheader(f'あなたが設定した目標は「{df_predicts2.iat[0,0]}」です')
                st.subheader(f'この目標が、具体的である確率は{con_p}%です。')
                st.subheader(f'この目標が、現実的である確率は{rea_p}%です。')




# elif page == 'answers':
#     st.write('answers')
#     # 回答内容の一覧の取得
#     works = crud.get_works(db=session)
#     works_list = {}
#     for work in works:
#         works_list[work.work_id] = {
#             'problem': work.problem,
#             'goal_q': work.goal_q,
#             'mq': work.mq,
#             'work_id': work.work_id
#         }
#     st.write(work)
#     df_works_list = pd.DataFrame(works_list)
#     st.table(df_works_list.T)


#     # 予測の一覧の取得
#     read_predict(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     predicts = crud.get_predicts(db, skip=skip, limit=limit)
#     return predicts
#     predicts_list = {}
#     for predict in predicts:
#         predicts_list[predict['predict_id']] = {
#             'goal_q': predict['goal_q'],
#             'con_01': predict['con_01'],
#             'con_p': predict['con_p'],
#             'rea_01': predict['rea_01'],
#             'rea_p': predict['rea_p']
#         }
#     st.write('### 予測の一覧')
#     df_predicts_list = pd.DataFrame(predicts_list)
#     st.table(df_predicts_list.T)

# elif page == 'test':
#     st.write('test')

# cd sfbt_test1
# uvicorn sql_setting.main:app --reload
# streamlit run app.py
