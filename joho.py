import streamlit as st
import pandas as pd
import numpy as np

st.title("初めてのstreamlit")
st.write("これから作品を作っていきます")

import time
st.sidebar.write('プログレスバーの表示')

latest_iteration = st.empty() #空コンテンツと一緒に変数を作成
bar = st.progress(0)#プログレスを作る 値は0


late = 0
for i in range(100):
    latest_iteration.text(f'読み込み中{i+1}%')#空のIterationにテキストを入れていく
    bar.progress(i+1)#barの中身をぐいぐい増やしていく
    late = (100 - i) / 10000
    time.sleep(late)

text = ""
text = st.text_input("あなたの名前を教えてください")
if text != "":
    st.write("あなたの名前は" +text+ "です")

option = st.selectbox("好きな数字を教えてください" ,list(["1番","2番","3番","4番"]))
st.write("あなたが選択したのは",option,"です")


left_column, right_column = st.columns(2)
button = left_column.button('右カラムに文字を表示')
if button:
    right_column.write('ここは右カラムです')

from PIL import Image #PILをpip install pillowを実施する
img = Image.open("kurea.png")
st.image(img, caption='増田來亜', use_container_width=True)

st.title("三角関数")
st.text("授業で使う三角関数がすぐに扱えるようにまとめました。度数法で入力してください。記号には対応していません。")
st.text("※√3/2→0.86603　1/√2→0.70711")

col1, col2, col3 =st.columns([1,1,1])

with col1:
    st.subheader("sin")
    text_5 = st.text_input("sinの値を求めます",key="text_5")
    if st.button("sin"):
        try:
            st.text(round(math.sin(math.radians(float(text_5))),5))
        except:
            st.text("この入力では処理できません。数字のみで入力をお願いします。")
    if st.button("asin"):
        try:
              st.text(int(math.degrees(math.asin(float(text_5)))))
        except:
            st.text("この入力では処理できません。数字のみで入力をお願いします。")

with col2:
    st.subheader("cos")
    text_6 = st.text_input("cosの値を求めます",key="text_6")
    if st.button("cos"):
        try:
            st.text(round(math.cos(math.radians(float(text_6))),5))
        except:
            st.text("この入力では処理できません。数字のみで入力をお願いします。")
    if st.button("acos"):
        try:
            st.text(int(math.degrees(math.acos(float(text_6)))))
        except:
            st.text("この入力では処理できません。数字のみで入力をお願いします。")

with col3:
    st.subheader("tan")
    text_7 = st.text_input("tanの値を求めます",key="text_7")
    if st.button("tan"):
        try:
            st.text(round(math.tan(math.radians(float(text_7))),5))
        except:
            st.text("この入力では処理できません。数字のみで入力をお願いします。")
    if st.button("atan"):
        try:
            st.text(round(math.degrees(math.atan(float(text_7))),5))
        except:
            st.text("この入力では処理できません。数字のみで入力をお願いします。")