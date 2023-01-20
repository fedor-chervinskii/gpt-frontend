import os, time
import logging
import openai
from flask import Blueprint, redirect, render_template, request, url_for, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled
from gpt_frontend.youtube_api import get_video_details


bp = Blueprint('summarize', __name__, url_prefix='/')
openai.api_key = os.getenv("OPENAI_API_KEY")

logging.basicConfig(level=logging.DEBUG)


MAX_WORDS_IN_VIDEO = 50000
MAX_WORDS_TO_USE_BIG_MODEL = 20000


@bp.route('/')
def index():
    return render_template("index.html", **request.args)


@bp.route('/loading', methods=['POST'])
def loading_model():
    return render_template("index.html", loading=True)


@bp.route('/summarize_video', methods=['POST'])
def summarize_video():
    video_url = request.form["video_url"]
    try:
        video_id = extract_youtube_video_id(video_url)
        video_title, thumbnail_url = get_video_details(video_id)
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_plain_text = " ".join(item["text"] for item in transcript)
        logging.debug("received transcript: {}".format(transcript_plain_text))

        #for capabilities and pricing see https://beta.openai.com/docs/models/gpt-3
        if request.form.get('big_model'):
            model = "text-davinci-003"
            max_words = 2000

        else:
            model = "text-curie-001"
            max_words = 1000

        logging.debug("using model: {}".format(model))

        results = {}

        if len(transcript_plain_text.split()) > MAX_WORDS_IN_VIDEO:
            raise ValueError("The video is too long to process, sorry...")

        if (len(transcript_plain_text.split()) > MAX_WORDS_TO_USE_BIG_MODEL and
            model == "text-davinci-003"):
            raise ValueError("""The video is too long to process with big model, sorry!
            Please try without using the slow and expensive model...""")

        for idx, block in enumerate(text_block_iterator(transcript_plain_text, max_words=max_words)):
            response = openai.Completion.create(
                model=model,
                prompt=generate_prompt(block),
                temperature=0.6,
                max_tokens=500,
            )
            logging.debug("received the response from OpenAI API: {}".format(response))
            results[idx] = str(response.choices[0].text)

        return render_template("index.html",
                               url=str(video_url),
                               video_title=video_title,
                               thumbnail_url=thumbnail_url,
                               results=results)

    except ValueError as error:
        logging.debug("received exception: {}".format(error))
        return redirect(url_for(
            "summarize.index",
            error_heading="There is a problem with the video",
            error_message=str(error)
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

    except openai.error.RateLimitError as error:
        logging.debug("received exception: {}".format(error))
        return redirect(url_for("summarize.index",
                                error_heading="API Rate Exceeded...",
                                error_message=str(error)))


def text_block_iterator(text, max_words=1500):
    words = text.split()
    num_words = len(words)
    if max_words > num_words:
        max_words = num_words
    overlap = int(max_words / 2)
    i = 0
    while i < num_words - max_words + 1:
        yield ' '.join(words[i:i+max_words])
        i += overlap
    if i < num_words:
        yield ' '.join(words[i:])


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