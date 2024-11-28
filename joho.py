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
