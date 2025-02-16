import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import chardet
from matplotlib import font_manager

def read_csv_with_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    encoding = result['encoding']
    return pd.read_csv(file_path, encoding=encoding)

# 日本語フォントの設定（Noto Sans CJK JP）
font_path = 'NotoSansCJK-Regular.ttc'  # アップロードしたフォントファイルのパス
font_prop = font_manager.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()

# CSVファイルから既存のデータを読み込みます
try:
    data = read_csv_with_encoding("coordinates.csv")
except FileNotFoundError:
    data = pd.DataFrame(columns=["X", "Y", "内容", "ジャンル", "道幅", "高さ", "凹凸", "障害物", "期間"])

try:
    word_data = read_csv_with_encoding("word_data.csv")
except FileNotFoundError:
    word_data = pd.DataFrame(columns=["あいことば", "車種", "全長", "全幅", "全高"])

tab71, tab72, tab73 = st.tabs(["マップ", "共有", "車体情報"])

with tab71:
    st.subheader("仮想マップ")

    if st.button("更新"):
        pass

    # フィルタリングスイッチ
    filter_by_vehicle = st.checkbox("車両情報でフィルタリング")

    # あいことばを入力して車両情報を取得
    input_word = st.text_input("あいことばを入力", key="input_word")
    vehicle_width = None
    if input_word and filter_by_vehicle:
        if input_word in word_data["あいことば"].values:
            vehicle_info = word_data[word_data["あいことば"] == input_word].iloc[0]
            vehicle_width = vehicle_info["全幅"]
        else:
            st.warning("指定されたあいことばが見つかりません")

    # 絞り込み機能
    filter_genre = st.selectbox("ジャンルで絞り込む", ["すべて"] + list(data["ジャンル"].unique()))
    if filter_genre != "すべて":
        if vehicle_width:
            filtered_data = data[(data["ジャンル"] == filter_genre) & 
                                 (data["道幅"].astype(float) >= vehicle_width)]
        else:
            filtered_data = data[data["ジャンル"] == filter_genre]
    else:
        if vehicle_width:
            filtered_data = data[data["道幅"].astype(float) >= vehicle_width]
        else:
            filtered_data = data

    # カラーマップの作成
    genre_colors = {
        "渋滞": "red",
        "抜け道": "blue",
        "通行止め": "green",
        "通りにくい": "orange",
        "事故": "purple",
        "災害": "brown"
    }

    # グラフの描画
    fig, ax = plt.subplots()
    for genre in filtered_data["ジャンル"].unique():
        genre_data = filtered_data[filtered_data["ジャンル"] == genre]
        ax.scatter(genre_data["X"], genre_data["Y"], c=genre_colors[genre], s=100, alpha=0.5, label=genre)

    for i, row in filtered_data.iterrows():
        ax.annotate(row["内容"], (row["X"], row["Y"]), textcoords="offset points", xytext=(0,10), ha='center', fontsize=8)
    ax.set_xlim(-100, 100)
    ax.set_ylim(-100, 100)
    ax.set_xlabel("X座標")
    ax.set_ylabel("Y座標")
    ax.grid(True)
    ax.legend()

    st.pyplot(fig)    

with tab72:
    genre = st.radio("ジャンル", ["渋滞", "抜け道", "通行止め", "通りにくい", "事故", "災害"])
    x_coord = st.number_input("X座標 (-100 - 100)", min_value=-100, max_value=100, step=1)
    y_coord = st.number_input("Y座標 (-100 - 100)", min_value=-100, max_value=100, step=1)
    new_content = st.text_input("内容")

    if genre == "通りにくい":
        roadsize1 = st.text_input("道幅")
        roadsize2 = st.text_input("高さ")
        roadsize3 = st.text_input("凹凸")
        roadsize4 = st.text_input("障害物")
    elif genre == "通行止め":
        roadstop = st.radio("期間", ["無期限", "選択"])
        if roadstop == "選択":
            roadstop2 = st.text_input("")

    if st.button("投稿"):
        try:
            new_data = pd.DataFrame({
                "X": [x_coord],
                "Y": [y_coord],
                "内容": [new_content],
                "ジャンル": [genre],
                "道幅": [roadsize1 if genre == "通りにくい" else None],
                "高さ": [roadsize2 if genre == "通りにくい" else None],
                "凹凸": [roadsize3 if genre == "通りにくい" else None],
                "障害物": [roadsize4 if genre == "通りにくい" else None],
                "期間": [roadstop2 if genre == "通行止め" and roadstop == "選択" else roadstop if genre == "通行止め" else None]
            })
            data = pd.concat([data, new_data], ignore_index=True)
            data.to_csv("coordinates.csv", index=False, encoding='utf-8')
            st.success("内容が登録されました")
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")

with tab73:
    tab11, tab12 = st.tabs(["編集", "削除"])

    with tab11:
        new_word = st.text_input("あいことばを入力", key="new_word")
        if new_word:
            if st.button("あいことばを確認"):
                if new_word not in word_data["あいことば"].values:
                    try:
                        new_data = pd.DataFrame({"あいことば": [new_word], "車種": [""], "全長": [""], "全幅": [""], "全高": [""]})
                        word_data = pd.concat([word_data, new_data], ignore_index=True)
                        word_data.to_csv("車種.csv", index=False, encoding='utf-8')
                    except Exception as e:
                        st.error(f"エラーが発生しました: {e}")
                else:
                    st.info("このあいことばは既に登録されています")

            if new_word in word_data["あいことば"].values:
                edit_data = word_data[word_data["あいことば"] == new_word]
                if not edit_data.empty:
                    edit_num = edit_data.index[0]
                    st.table(edit_data)
                    edi_wo = st.checkbox("車種を編集")
                    if edi_wo:
                        edit_word = st.text_input("編集する車種")
                    st.divider()
                    edi_me = st.checkbox("全長を編集")
                    if edi_me:
                        edit_meaning = st.text_input("編集する全長")
                    st.divider()
                    edi_re = st.checkbox("全幅を編集")
                    if edi_re:
                        edit_remembered = st.text_input("編集する全幅")
                    st.divider()
                    edi_kou = st.checkbox("全高を編集")
                    if edi_kou:
                        edit_zenkou = st.text_input("編集する全高")
                    if edi_wo or edi_me or edi_re or edi_kou:
                        if st.button("登録内容を修正"):
                            try:
                                if edi_wo:
                                    word_data.at[edit_num, "車種"] = edit_word
                                if edi_me:
                                    word_data.at[edit_num, "全長"] = edit_meaning
                                if edi_re:
                                    word_data.at[edit_num, "全幅"] = edit_remembered
                                if edi_kou:
                                    word_data.at[edit_num, "全高"] = edit_zenkou
                                word_data.to_csv("車種.csv", index=False, encoding='utf-8')
                                st.success("修正に成功しました！")
                            except Exception as e:
                                st.error(f"修正に失敗しました: {e}")

    with tab12:
        delete_word = st.text_input("削除するあいことばを入力", key="delete_word")
        if delete_word:
            if st.button("あいことばを削除", key="delete_button"):
                if delete_word in word_data["あいことば"].values:
                    try:
                        word_data = word_data[word_data["あいことば"] != delete_word]
                        word_data.to_csv("車種.csv", index=False, encoding='utf-8')
                        st.success("削除に成功しました")
                    except Exception as e:
                        st.error(f"削除に失敗しました: {e}")
                else:
                    st.warning("指定されたあい言葉が見つかりません")
