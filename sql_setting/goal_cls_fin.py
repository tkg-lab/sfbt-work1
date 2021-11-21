
import torch
from transformers import BertJapaneseTokenizer, BertForSequenceClassification
import streamlit as st
import os

@st.cache(show_spinner=False)
def predict(text):
  MODEL_NAME = 'cl-tohoku/bert-base-japanese-whole-word-masking'

  tokenizer = BertJapaneseTokenizer.from_pretrained(MODEL_NAME)

  cls_text = []
  cls_text.append(text)
  
  model_path = os.path.dirname(os.path.abspath(__file__))
  
  bert_sc_con = BertForSequenceClassification.from_pretrained(
      f'{model_path}\model_12e0_34e1_con'
  )
  bert_sc_rea = BertForSequenceClassification.from_pretrained(
      f'{model_path}\model_0e0_12e0_34e1_rea'
  )
  
  encoding = tokenizer(
      cls_text,
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

  for text, con_01, con_p, rea_01, rea_p in zip(cls_text, con_predicted, con_percent, rea_predicted, rea_percent):
    resp = {}
    resp["goal_q"] = text
    resp["con_01"] = con_01.item()
    resp["con_p"] = con_p[1].item()
    resp["rea_01"] = rea_01.item()
    resp["rea_p"] = rea_p[1].item()
  return resp


@st.cache(show_spinner=False)
def predict_2(text):
  MODEL_NAME = 'cl-tohoku/bert-base-japanese-whole-word-masking'

  tokenizer = BertJapaneseTokenizer.from_pretrained(MODEL_NAME)

  cls_text = []
  cls_text.append(text)
  
  model_path = os.path.dirname(os.path.abspath(__file__))
  
  bert_sc_con = BertForSequenceClassification.from_pretrained(
      f'{model_path}\model_12e0_34e1_con'
  )
  bert_sc_rea = BertForSequenceClassification.from_pretrained(
      f'{model_path}\model_0e0_12e0_34e1_rea'
  )
  encoding = tokenizer(
      cls_text,
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

  for text, con_01, con_p, rea_01, rea_p in zip(cls_text, con_predicted, con_percent, rea_predicted, rea_percent):
    resp = {}
    resp["goal_reset"] = text
    resp["con_01"] = con_01.item()
    resp["con_p"] = con_p[1].item()
    resp["rea_01"] = rea_01.item()
    resp["rea_p"] = rea_p[1].item()
  return resp

# conda install -c conda-forge transformers==4.5.0
# conda install pytorch torchvision -c pytorch
# pip -c conda-forge fugashi
# pip -c conda-forge ipadic==1.0.0
