import streamlit as st
import requests
import pandas as pd
from utils import fetch_topics, LANGUAGE_LIST, extract_topic_ids

BASE_URL = "https://birdxplorer.onrender.com/api/v1/data/notes"

# 説明を書く
st.header("Community Notes Viewer")
st.write("コミュニティノートのデータを取得するためのツールです。")
st.link_button("詳細はドキュメントへ", "https://birdxplorer.onrender.com/docs#/default/get_notes_api_v1_data_notes_get")

topics = fetch_topics()

# APIパラメータの入力
offset = st.number_input("Offset", min_value=0, value=0, step=1)
limit = st.number_input("Limit", min_value=1, max_value=1000, value=5, step=1)
language = st.selectbox("Language", LANGUAGE_LIST)
note_ids = st.text_area("Note IDs (comma separated)", placeholder="1846124913612226626,1846257106212815006")
created_at_from = st.text_input("Created At From (UNIX EPOCH TIME in ms)", placeholder="1730638628907")
created_at_to = st.text_input("Created At To (UNIX EPOCH TIME in ms)", placeholder="1730638628907")
topic_ids = st.multiselect("Topic IDs", list(topics.keys()))
post_ids = st.text_input("Post IDs (comma separated)", placeholder="1846124913612226626,1846257106212815006")
current_status = st.multiselect(
    "Current Status",
    options=["NEEDS_MORE_RATINGS", "CURRENTLY_RATED_HELPFUL", "CURRENTLY_RATED_NOT_HELPFUL"],
    default=[]
)

if st.button("データを取得する"):
    params = {
        "offset": offset,
        "limit": limit,
        "topic_ids": [],
        "post_ids": []
    }
    if note_ids:
        params["note_ids"] = note_ids.split(",")
    if created_at_from:
        params["created_at_from"] = created_at_from
    if created_at_to:
        params["created_at_to"] = created_at_to
    if topic_ids:
        params["topic_ids"] = [topics[topic_id] for topic_id in topic_ids]
    if post_ids:
        params["post_ids"] = post_ids.split(",")
    if language:
        params["language"] = language
    if current_status:
        params["current_status"] = current_status

    # APIへのリクエスト
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        # データの表示
        if "data" in data:
            st.write("Fetched Notes:")
            notes = data["data"]

            # データをDataFrameに変換
            df = pd.DataFrame(notes)
            st.dataframe(df)

            # 'topics'列については、トピックIDをトピック名に変換
            df["topics"] = df["topics"].apply(lambda x: [item['topicId'] for item in x] if isinstance(x, dict) else [])

            # 
            df['topics'] = df['topics'].apply(extract_topic_ids)

            # データのダウンロード
            st.download_button(
                label="Download Data as CSV",
                data=df.to_csv(index=False).encode(),
                file_name="notes.csv",
                mime="text/csv"
            )
        else:
            st.write("No data found.")

    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {e}")
