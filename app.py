from flask import Flask, redirect, url_for, request, render_template, session
import requests, os, uuid, json
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
  return render_template('index.html')

@app.route('/', methods=['POST'])
def index_post():
  original_text = request.form['text']
  target_language = request.form['language']

  endpoint = os.environ['ENDPOINT']
  location = os.environ['LOCATION']
  key = os.environ['KEY']

  path = '/translate?api-version=3.0'
  target_language_parameter = '&to=' + target_language
  constructed_url = endpoint + path + target_language_parameter

  headers = {
    'Ocp-Apim-Subscription-Key': key,
    'Ocp-Apim-Subscription-Region': location,
    'Content-type':'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
  }

  body = [{ 'text': original_text}]

  translator_request = requests.post(constructed_url, headers=headers, json=body)
  translator_response = translator_request.json()
  translated_text = translator_response[0]['translations'][0]['text']

  return render_template(
      'results.html',
      original_text=original_text,
      translated_text=translated_text,
      target_language=target_language
    )

if __name__ == '__main__':
  app.run(debug=True)