import re
import os 
from flask import Flask, render_template, json, send_from_directory


app = Flask(__name__, template_folder="templates", static_folder="static")

def clean_text(text):
    text = re.sub(r'@\w+', '', text)
    text = re.sub(r'#\S+', '', text)
    return text.strip()

@app.route('/')
def index():
    with open('data/tweets_with_sentiment.json', encoding='utf-8') as f:
        raw_data = json.load(f)

    tweets = []
    for item in raw_data:
        cleaned = clean_text(item.get('text_cleaned', ''))
        if not cleaned or cleaned == "":
            continue
        tweets.append({
            'timestamp': item.get('timestamp'),
            'text': cleaned,
            'sentiment': item.get('sentiment'),
            'score': round(item.get('score', 0.0) * 100, 1)
        })

    return render_template('index.html', tweets=tweets)

if __name__ == '__main__':
    os.environ['FLASK_APP'] = 'app.py'
    os.environ['FLASK_ENV'] = 'development'
    app.run(debug=True)