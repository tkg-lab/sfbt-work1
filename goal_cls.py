
import torch
from transformers import BertJapaneseTokenizer, BertForSequenceClassification

MODEL_NAME = 'cl-tohoku/bert-base-japanese-whole-word-masking'

tokenizer = BertJapaneseTokenizer.from_pretrained(MODEL_NAME)

max_length = 128
dataset_for_loader = []

path = './sfbt_test1/data/ana_ex_goal_e210702a.tsv'  # フォルダの場所を指定

text_list = ["仕事を終わらせる", "朝5時に起きられるようになる", "毎夕、ジョギングする", "読みたい本の1か月に5冊読む", "試験勉強を毎日30分以上続ける", "完全に自己承認ができている自分になる", "毎日8時間、きっちり寝る", "体重を1か月で2キロ減らす"]

bert_sc_con = BertForSequenceClassification.from_pretrained(
    './sfbt_test1/model_12e0_34e1_con'
)

bert_sc_rea = BertForSequenceClassification.from_pretrained(
    './sfbt_test1/model_0e0_12e0_34e1_rea'
)

encoding = tokenizer(
    text_list,
    padding = 'longest',
    return_tensors='pt'
)
encoding = { k: v for k, v in encoding.items() }

with torch.no_grad():
  output_con = bert_sc_con(**encoding)
  output_rea = bert_sc_rea(**encoding)
con_predicted = output_con.logits.argmax(-1)
con_percent = output_con.logits.softmax(-1)

rea_predicted = output_rea.logits.argmax(-1)
rea_percent = output_rea.logits.softmax(-1)


for text, con_01, con_p, rea_01, rea_p in zip(text_list, con_predicted, con_percent, rea_predicted, rea_percent):
  print('--')
  print(f'入力: {text}')
  print(f'具体性の予測ラベル: {con_01}')
  print(f'「具体性がない」に該当する確率: {con_p[0]}')
  print(f'「具体性がある」に該当する確率: {con_p[1]}')
  print(f'実現可能性の予測ラベル: {rea_01}')
  print(f'「実現可能性がない」に該当する確率: {rea_p[0]}')
  print(f'「実現可能性がある」に該当する確率: {rea_p[1]}')

# conda install -c conda-forge transformers==4.5.0
# conda install pytorch torchvision -c pytorch
# pip -c conda-forge fugashi
# pip -c conda-forge ipadic==1.0.0
