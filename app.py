from unicodedata import category
import json
from urllib import response
from sklearn.utils import resample
from ai.main import ai
from flask import Flask, render_template, request, send_from_directory, flash, redirect, url_for
import pandas as pd
from ai.main import ai
from twitter.twcontroller import getTweetsByUser, getTweet, searchTweets
import os
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = './data'
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__, static_url_path='/static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/uploadFile', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # iaResults = analizarYResponder(filename)
            textos = textosDocumentos(filename)
            respuesta = '{"textos":' + json.dumps(textos) + '}'
            return respuesta
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


@app.route('/download')
def download_file():
    return send_from_directory(app.config["UPLOAD_FOLDER"], 'testExample.csv')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/twitter')
def twitter():
    return render_template('twitter.html')


@app.route('/getTweetsByUsername', methods=['POST'])
def getTweetsByUsername():
    if request.method == 'POST':
        username = request.form.get("data")
        tweets = getTweetsByUser(username)
        train = pd.DataFrame(tweets, columns=['id', 'text'])
        train.to_csv('./data/test2.csv', index=False)
        data = []
        for tweet in tweets:
            data.append(tweet[1])
        return json.dumps(data)


@app.route('/getTweetByLink', methods=['POST'])
def getTweetByLink():
    if request.method == 'POST':
        enlace = request.form.get("data")
        id = enlace.split('/')[5]
        tweet = getTweet(id)
        train = pd.DataFrame(tweet, columns=['id', 'text'])
        train.to_csv('./data/test2.csv', index=False)
        data = []
        for twet in tweet:
            data.append(twet[1])
        return json.dumps(data)


@app.route('/checkMessage', methods=['POST'])
def checkMessage():
    if request.method == 'POST':
        textos = request.form.getlist("textos[]")
        formatData = []
        for i in range(len(textos)):
            formatData.append([i, textos[i]])

        train = pd.DataFrame(formatData, columns=['id', 'text'])
        train.to_csv('./data/test2.csv', index=False)
    response = analizarYResponder()
    return response


@app.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        searchParam = request.form.get("data")
        dataSet = searchTweets(searchParam)
        train = pd.DataFrame(dataSet, columns=['id', 'text'])
        train.to_csv('./data/test2.csv', index=False)
        data = []
        for tweet in dataSet:
            data.append(tweet[1])
    return json.dumps(data)


@app.route("/static/<path:path>")
def static_dir(path):
    return send_from_directory("static", path)


@app.route('/analizar/<path>',  defaults={'path': 'test2.csv'},  methods=['POST'])
def analizar(path):
    respuesta = analizarYResponder(path)
    return respuesta


def textosDocumentos(path):
    data = pd.read_csv('./data/'+path, sep=',')
    textos = []
    for index, row in data.iterrows():
        textos.append(str(row['text']))
    return textos


def analizarYResponder(pathDocument='test2.csv'):
    ai("label", 'train.csv', pathDocument)
    ai("category1", 'train_category1.csv', pathDocument)
    ai("category2", 'train_category2.csv', pathDocument)
    ai("category3", 'train_category3.csv', pathDocument)
    ai("category4", 'train_category4.csv', pathDocument)
    ai("single", 'train_single.csv', pathDocument)
    ai("groups", 'train_groups.csv', pathDocument)

    label = pd.read_csv('submissions/lr_submission_label.csv')
    category1 = pd.read_csv('submissions/lr_submission_category1.csv')
    category2 = pd.read_csv('submissions/lr_submission_category2.csv')
    category3 = pd.read_csv('submissions/lr_submission_category3.csv')
    category4 = pd.read_csv('submissions/lr_submission_category4.csv')
    single = pd.read_csv('submissions/lr_submission_single.csv')
    groups = pd.read_csv('submissions/lr_submission_groups.csv')

    labelResults = []
    category1Results = []
    category2Results = []
    category3Results = []
    category4Results = []
    singleResults = []
    groupsResults = []

    for index, row in label.iterrows():
        labelResults.append(str(row['label']))
    labelResults = ",".join(labelResults)

    for index, row in category1.iterrows():
        category1Results.append(str(row['category1']))
    category1Results = ",".join(category1Results)

    for index, row in category2.iterrows():
        category2Results.append(str(row['category2']))
    category2Results = ",".join(category2Results)

    for index, row in category3.iterrows():
        category3Results.append(str(row['category3']))
    category3Results = ",".join(category3Results)

    for index, row in category4.iterrows():
        category4Results.append(str(row['category4']))
    category4Results = ",".join(category4Results)

    for index, row in single.iterrows():
        singleResults.append(str(row['single']))
    singleResults = ",".join(singleResults)

    for index, row in groups.iterrows():
        groupsResults.append(str(row['groups']))
    groupsResults = ",".join(groupsResults)

    response = '{"label":[' + labelResults + '],"category1":[' + category1Results + '],"category2":[' + category2Results + '],"category3":[' + \
        category3Results + '] ,"category4":[' + category4Results + \
        '],"single":[' + singleResults + \
        '], "groups":[' + groupsResults + ']}'
    return response


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
