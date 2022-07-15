from flask import Flask
from datetime import *
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter
import json

app = Flask(__name__)


def get_transcript(video_id, language=None):
    if language is None:
        language = ['en']

    script = YouTubeTranscriptApi.get_transcript(video_id, language)
    formatter = JSONFormatter()
    json_formatted = formatter.format_transcript(script)
    json_object = json.loads(json_formatted)
    text = ''
    for entry in json_object:
        text += entry['text'] + ' '
    return text 




app.route('/')
def index():
    return "Hello world!"

def main():
    get_transcript('j6PbonHsqW0')


if __name__ == '__main__':
    # app.run()
    main()
