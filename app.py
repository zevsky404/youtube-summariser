from flask import Flask
from datetime import *
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter
import json

app = Flask(__name__)

"""
takes a video id for a YouTube video, fetches all available transcripts available for it and finds the English one
or translates the first available transcript into English, if possible. It then parses the returned object and returns 
the text of the transcript.
@:param video-id: video ID of YouTube video
@:return: transcript of the YouTube video
"""


def get_transcript(video_id):
    script_list = YouTubeTranscriptApi.list_transcripts(video_id)
    try:
        script = script_list.find_transcript(['en'])
        final_script = script.fetch()
    except:
        script = script_list[0]
        if script.is_translatable:
            translated_script = script.translate('en')
            final_script = translated_script.fetch()
        else:
            print("Script for this video is not available and also not translatable into English.")
    formatter = JSONFormatter()
    json_formatted = formatter.format_transcript(final_script)
    json_object = json.loads(json_formatted)
    text = ''
    for entry in json_object:
        text += entry['text'] + ' '
    return text




app.route('/')
def index():
    return "Hello world!"

def main():
    print(get_transcript('tRBeGm0QMvU'))


if __name__ == '__main__':
    # app.run()
    main()
