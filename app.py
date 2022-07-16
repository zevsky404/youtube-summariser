# backend imports
from flask import Flask
from datetime import *
# YouTube transcript imports
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter
# transformer imports
from transformers import T5ForConditionalGeneration, T5Tokenizer
# utility imports
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
    # fetch list of available transcripts
    script_list = YouTubeTranscriptApi.list_transcripts(video_id)
    try:
        # find English transcript
        script = script_list.find_transcript(['en'])
        final_script = script.fetch()
    except:
        # translate first available transcript into English
        script = script_list[0]
        if script.is_translatable:
            translated_script = script.translate('en')
            final_script = translated_script.fetch()
        else:
            print("Script for this video is not available and also not translatable into English.")
    # format TranscriptObject into JSON and parse the text into a single string
    formatter = JSONFormatter()
    json_formatted = formatter.format_transcript(final_script)
    json_object = json.loads(json_formatted)
    text = ''
    for entry in json_object:
        text += entry['text'] + ' '
    return text


def summarise_transcript(transcript):
    # initialise model architecture and weights
    model = T5ForConditionalGeneration.from_pretrained("t5-base")
    # initialise model tokenizer
    tokenizer = T5Tokenizer.from_pretrained("t5-base")
    # encode text for the model
    encoded = tokenizer.encode("summarize: " + transcript, return_tensors="pt", max_length=512, truncation=True)
    encoded_summary = model.generate(
        encoded,
        max_length=200,
        min_length=40,
        length_penalty=2.0,
        num_beams=4,
        early_stopping=True
    )
    return tokenizer.decode(encoded_summary[0])


app.route('/')
def index():
    return "Hello world!"


def main():
    transcript = get_transcript('L3sAQVIa9n8')
    print(summarise_transcript(transcript))


if __name__ == '__main__':
    # app.run()
    main()
