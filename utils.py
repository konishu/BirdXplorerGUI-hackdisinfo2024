import requests

TOPIC_URL = "https://birdxplorer.onrender.com/api/v1/data/topics"

def fetch_topics():
    try:
        response = requests.get(TOPIC_URL)
        response.raise_for_status()
        data = response.json()['data']
        # return {f"{topic['topicId']}:{topic['label']['ja']}/{topic['label']['en']}": topic['topicId'] for topic in data}
        return {str(str(topic['topicId'])+ ":" + topic['label']['ja']+"/" + topic['label']['en']):topic['topicId'] for topic in data}
    except requests.exceptions.RequestException as e:
        return []
    


LANGUAGE_LIST = [
    "ja","en", "es",  "pt", "de", "fr", "fi", "tr", "nl", "he", "it", "fa", "ca", "ar", "el", "sv", "da", "ru", "pl", "other"
]
