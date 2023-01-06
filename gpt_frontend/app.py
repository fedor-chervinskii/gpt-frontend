import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = create_app()
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route('/')
def index():
    return 'Hello, World!'
#    result = request.args.get("result")
#    return render_template("index.html", result="")


@app.route('/api/summarize_text', methods=['POST'])
def summarize_text():
    text = request.form["text"]
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=generate_prompt(text),
        temperature=0.6,
    )
    return redirect(url_for("index", result=response.choices[0].text))


def generate_prompt(text):
    return """summarize the following text in one sentence: """.format(
        text
    )
