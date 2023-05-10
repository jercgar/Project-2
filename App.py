from flask import Flask, url_for, render_template, redirect

app = Flask(__name__)


@app.route("/", methods=['GET'])
def index():

    return render_template('index.html')


@app.route("/about", methods=['GET'])
def about():

    return render_template('about.html')
