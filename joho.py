import streamlit as st
import requests
import math
from PIL import Image
import pandas as pd
import datetime
import pytz

st.title("もの技ツール集 Ver.2")

tab0, tab1, tab2, tab3, tab4, tab5, tab6= st.tabs(["概要","文字数","置換","連絡先","三角関数","画像変換","単語帳"])

with tab0:
    st.header("概要")
    st.text("このサイトでは大学生活でたまに使う細かいツールを集めてみました。これ一つで様々なことができます。2年弱、もの技で過ごしてきて使ったツールをまとめてみたのでぜひ活用してください。")
    st.divider()
    api_key = "07e67ab7542092483c720629da6e0542"
    col4, col5 = st.columns(2)
    with col4:
        try:
            japan_tz = pytz.timezone("Asia/Tokyo")
            df_now = datetime.datetime.now(japan_tz)
            st.subheader(f"{df_now.year}年 {df_now.month}月 {df_now.day}日")
            st.subheader(f"{df_now.hour}時 {df_now.minute}分")
            st.subheader(f"令和{(df_now.year)-2018}年")
        except:
            st.text("エラーが発生しました")
    with col5:
        try:
            cities = ["Nagano","Matsumoto","Ueda","Ina"]
            city_name = ["長野","松本","上田","伊那"]
            df_we = pd.DataFrame({"天気":[None,None,None,None],"気温":[None,None,None,None],})
            df_we.index = city_name
            def get_weather(city, api_key):
                url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
                response = requests.get(url)
                data = response.json()
                return data
            for city in cities:
                data = get_weather(city, api_key)
                if data.get("weather"):
                    df_we.at[city_name[cities.index(city)],"天気"] = data['weather'][0]['description']
                    df_we.at[city_name[cities.index(city)],"気温"] = data['main']['temp']
            st.write(df_we)
        except:
            st.text("エラーが発生しました")
    if st.button("更新"):
        pass

with tab1:
    st.header("文字数チェッカー")
    st.text("文字数を数えます。")
    st.divider()
    text_1 = st.text_input("ここにテキストを入れてください",key="text_1")
    df = pd.read_csv("Book1.csv")
    if text_1:
        st.subheader(str(len(text_1))+"文字")
        if any(df["列1"]==text_1):
            df_num = df.index[df["列1"]==text_1]
            st.text(df.iloc[df_num,1].values[0])

with tab2:
    st.header("置換")
    st.text("文章内の文字を置き換えます。")
    st.divider()
    text_3 = st.text_input("元の文章を入れてください",key="text_3")
    repB = st.text_input("置換前",key="repB")
    repA = st.text_input("置換後",key="repA")
    if text_3:
        if st.button("、。を,.に置換"):
            text_4 = text_3.replace("、",",")
            text_4 = text_4.replace("。",".")
            st.text(text_4)
    if text_3:
        if st.button(",.を、。に置換"):
            text_4 = text_3.replace(",","、")
            text_4 = text_4.replace("，","、")
            text_4 = text_4.replace(".","。")
            text_4 = text_4.replace("．","。")
            st.text(text_4)
    if text_3 and repB:
        if st.button("置換"):
            text_4 = text_3.replace(repB,repA)
            st.text(text_4)

with tab3:
    st.header("連絡先")
    st.text("この項目は削除しました")
    
    

with tab4:
    st.title("三角関数")
    st.text("授業で使う三角関数がすぐに扱えるようにまとめました。度数法で入力してください。記号には対応していません。")
    st.divider()
    st.text("※√3/2→0.86603 1/√2→0.70711")
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

with tab5:
    st.title("画像サイズ")
    st.text("画像サイズを変換します。")
    st.divider()
    fileb = st.file_uploader("画像ファイルを選択してください",type=["png","jpg","webp"])
    if fileb is not None:
        try:
            file_name = fileb.name
            photob = Image.open(fileb)
            width,height = photob.size
            st.text("横:"+str(width)+",縦:"+str(height))
        except:
            st.text("エラーが発生しました")
    format = st.radio("ファイル形式",("jpg","png"),horizontal=True)
    if st.button("600以下で変換"):
        try:
            if width >= height :
                photoa = photob.resize((600,int(height*(600/width))))
            else:
                photoa = photob.resize((int(width*(600/height)),600))
            if format == "jpg":
                photoa = photoa.convert("RGB")
            else:
                photoa = photoa.convert("RGBA")
            st.image(photoa,caption="変換完了",use_container_width=True)
        except:
            st.text("エラーが発生しました")
    st.divider()
    photo_sizeW = st.slider("横の変換後のサイズ",100,1200,600)
    photo_sizeH = st.slider("縦の変換後のサイズ",100,1200,600)
    if st.button("指定のサイズで変換"):
        try:
            photoa = photob.resize((photo_sizeW,photo_sizeH))
            if format == "jpg":
                photoa = photoa.convert("RGB")
            else:
                photoa = photoa.convert("RGBA")
            st.image(photoa,caption=" 変換完了",use_container_width=True)    
        except:
            st.text("エラーが発生しました")

with tab6:
    st.title("単語帳")
    st.text("単語とその意味、理解しているかどうかを記録します。")
    st.divider()
    word_data = pd.read_csv("word.csv")
    st.table(word_data)
    if st.button("更新",key="word"):
        pass
    tab10, tab11, tab12 = st.tabs(["追加","編集","削除"])
    with tab10:
        new_word = st.text_input("新しく登録する単語",key="new_word")
        new_meaning = st.text_input("新しく登録する単語の意味",key="new_meaning")
        new_remembered = st.checkbox("理解した",key="new_remembered")
        if new_word and new_meaning:
            if st.button("単語を追加"):
                if new_remembered == False:
                    new_remembered = "×"
                elif new_remembered == True:
                    new_remembered = "〇"
                else:
                    new_remembered = "-"
                try:
                    new_data = pd.DataFrame({"単語": [new_word],"意味": [new_meaning],"理解": [new_remembered]})
                    word_data = pd.concat([word_data, new_data], ignore_index=True)
                    word_data.to_csv("word.csv",index=False)
                    st.success("単語の追加に成功しました！")
                except:
                    st.error("単語の追加に失敗しました")
    with tab11:
        edit_remembered = None
        edit_words = st.selectbox("編集する単語を選択", word_data["単語"],key="edit_words")
        edit_num = word_data.index[word_data["単語"] == edit_words].tolist()[0]
        st.table(word_data.loc[edit_num].to_frame().T)
        edi_wo = st.checkbox("単語を編集")
        if edi_wo:
            edit_word = st.text_input("編集する単語")
        st.divider()
        edi_me = st.checkbox("意味を編集")
        if edi_me:
            edit_meaning = st.text_input("編集する意味")
        st.divider()
        edi_re = st.checkbox("理解を編集")
        if edi_re:
            edit_remembered = st.radio("",options=["理解した","理解していない"])
        if edi_wo or edi_me or edi_re:
            if st.button("単語を修正"):
                if edit_remembered == "理解していない":
                    edit_remembered = "×"
                elif edit_remembered == "理解した":
                    edit_remembered = "〇"
                else:
                    edit_remembered = "-"
                try:
                    if edi_wo:
                        word_data.at[edit_num, "単語"] = edit_word
                    if edi_me:
                        word_data.at[edit_num, "意味"] = edit_meaning
                    if edi_re:
                        word_data.at[edit_num, "理解"] = edit_remembered
                    word_data.to_csv("word.csv",index=False)
                    st.success("修正に成功しました！")
                except:
                    st.error("修正に失敗しました")
    with tab12:
        delete_words = st.selectbox("削除する単語を選択", word_data["単語"], key="delete_words")
        if st.button("単語を削除", key="delete_button"):
            try:
                word_data = word_data[word_data["単語"] != delete_words]
                word_data.to_csv("word.csv", index=False)
                st.success("削除に成功しました！")
            except Exception as e:
                st.error("削除に失敗しました")