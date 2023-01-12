import os
import logging
import openai
from flask import Blueprint, redirect, render_template, request, url_for, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled

bp = Blueprint('summarize', __name__, url_prefix='/')
openai.api_key = os.getenv("OPENAI_API_KEY")

logging.basicConfig(level=logging.DEBUG)


@bp.route('/')
def index():
    return render_template("index.html", **request.args)


@bp.route('/api/summarize_text', methods=['POST'])
def summarize_text():
    text = request.form["text"]
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=generate_prompt(text),
        temperature=0.6,
        max_tokens=1000,
    )
    return redirect(url_for("summarize.index", result=response.choices[0].text))


@bp.route('/api/summarize_video', methods=['POST'])
def summarize_video():
    video_url = request.form["video_url"]
    try:
        video_id = extract_youtube_video_id(video_url)
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_plain_text = " ".join(item["text"] for item in transcript)
        logging.debug("received transcript: {}".format(transcript_plain_text))
        #response = transcript_plain_text

        #for capabilities and pricing see https://beta.openai.com/docs/models/gpt-3
        if request.form.get('big_model'):
            model = "text-davinci-003"

        else:
            model = "text-curie-001"
        logging.debug("using model: {}".format(model))

        response = openai.Completion.create(
            model=model,
            prompt=generate_prompt(transcript_plain_text),
            temperature=0.6,
            max_tokens=1000,
        )
        logging.debug("received the response from OpenAI API: {}".format(response))
        return redirect(url_for("summarize.index",
                                url=str(video_url),
                                result=str(response.choices[0].text)
                                ))
    except TranscriptsDisabled as error:
        logging.debug("received exception: {}".format(error))
        return redirect(url_for(
            "summarize.index",
            error_heading="Could not retrieve a transcript...",
            error_message=str(error)
        ))
    except openai.error.InvalidRequestError as error:
        logging.debug("received exception: {}".format(error))
        return redirect(url_for("summarize.index",
                                error_heading="Sorry, the video is too long...",
                                error_message=str(error)))


def extract_youtube_video_id(video_url):
    if "=" in video_url:
        video_id = (video_url.split('=')[1]).split("&")[0]
    else:
        video_id = video_url.split("/")[-1]
    return video_id


def generate_prompt(text):
    return """The following is the video transcript: {}. Summary of the video in one sentence is:""".format(
        text
    )