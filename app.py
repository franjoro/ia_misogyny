from unicodedata import category
import json
from sklearn.utils import resample
from ai.main import ai
from flask import Flask, render_template, request, send_from_directory
import pandas as pd
from ai.main import ai
from twitter.twcontroller import getTweetsByUser, getTweet, searchTweets

app = Flask(__name__, static_url_path='/static')


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


@app.route('/analizar', methods=['POST'])
def analizar():
    respuesta = analizarYResponder()
    return respuesta


def analizarYResponder():
    ai("label", 'train.csv')
    ai("category1", 'train_category1.csv')
    ai("category2", 'train_category2.csv')
    ai("category3", 'train_category3.csv')
    ai("category4", 'train_category4.csv')
    ai("single", 'train_single.csv')
    ai("groups", 'train_groups.csv')

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
