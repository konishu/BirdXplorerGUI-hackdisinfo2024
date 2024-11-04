import streamlit as st
import requests
import pandas as pd
from utils import fetch_topics, LANGUAGE_LIST

BASE_URL = "https://birdxplorer.onrender.com/api/v1/data/posts"

# 説明を書く
st.header("Community Notes Viewer")
st.write("コミュニティノートが作成された投稿を取得するツールです。")
st.link_button("詳細はドキュメントへ", "https://birdxplorer.onrender.com/docs#/default/get_posts_api_v1_data_posts_get")

topics = fetch_topics()

# APIパラメータの入力
offset = st.number_input("Posts Offset", min_value=0, value=0, step=1)
limit = st.number_input("Posts Limit", min_value=1, max_value=1000, value=5, step=1)
post_ids = st.text_area("Post IDs (comma separated)", placeholder="1846124913612226626,1846257106212815006")
note_ids = st.text_area("Note IDs (comma separated)", placeholder="1846124913612226626,1846257106212815006")
user_ids = st.text_area("User IDs (comma separated)", placeholder="12345,67890")
created_at_from = st.text_input("Created At From (UNIX EPOCH TIME in ms)", placeholder="1730638628907")
created_at_to = st.text_input("Created At To (UNIX EPOCH TIME in ms)", placeholder="1730638628907")
language = st.selectbox("Language", LANGUAGE_LIST)
search_text = st.text_input("Search Text", placeholder="Search within post content")
search_url = st.text_input("Search URL", placeholder="https://example.com")
media = st.checkbox("Include Media Information", value=True)

# リクエストを送信するボタン
if st.button("データを取得する"):
    # クエリパラメータの構築
    params = {
        "offset": offset,
        "limit": limit,
        "media": media
    }
    if post_ids:
        params["post_ids"] = post_ids.split(",")
    if note_ids:
        params["note_ids"] = note_ids.split(",")
    if user_ids:
        params["user_ids"] = user_ids.split(",")
    if created_at_from:
        params["created_at_from"] = created_at_from
    if created_at_to:
        params["created_at_to"] = created_at_to
    if language:
        params["language"] = language
    if search_text:
        params["search_text"] = search_text
    if search_url:
        params["search_url"] = search_url

    # APIへのリクエスト
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        # データの表示
        if "data" in data:
            st.write("Fetched Posts:")
            posts = data["data"]  # データをリスト形式に変換

            # データをDataFrameに変換
            df = pd.DataFrame(posts)
            
            df['user_userId'] = df['xUser'].apply(lambda x: x['userId'])
            df['user_name'] = df['xUser'].apply(lambda x: x['name'])
            df['user_profileImage'] = df['xUser'].apply(lambda x: x['profileImage'])
            df['user_followersCount'] = df['xUser'].apply(lambda x: x['followersCount'])
            df['user_followingCount'] = df['xUser'].apply(lambda x: x['followingCount'])
            df.drop(['xUser'], axis=1, inplace=True)

            st.dataframe(df)

            # データのダウンロード
            st.download_button(
                label="Download Data as CSV",
                data=df.to_csv(index=False).encode(),
                file_name="posts.csv",
                mime="text/csv"
            )
        else:
            st.write("No data found.")

    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {e}")
