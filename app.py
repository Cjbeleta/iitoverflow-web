import flask
import sys
import os
import requests
from datetime import datetime
#from urllib.parse import quote
from urllib import urlopen, quote
from flask import Flask, render_template, request, session, redirect, url_for, jsonify, json

app = Flask(__name__)
app.secret_key = 'my very own secret key'
app.config['SESSION_TYPE'] = 'filesystem'


@app.route('/')
def index():
    return render_template('landingpage2.html')


@app.route('/categories', methods=['POST', 'GET'])
def fillup():
    if request.method == 'POST':
        data = request.get_json()
        ids = data['ids']
        for i in ids:
            requests.post('http://iitoverflow.herokuapp.com/api/Interests',
                          json={"categoryId": i, "userId": 1})

        return jsonify({"message":"okay"})

    else:
        url = ('http://iitoverflow.herokuapp.com/api/Categories')
        response = requests.get(url)
        categories = response.json()

        return render_template('Categories.html', categories=categories)


@app.route('/login', methods=['POST'])
def login():
    params = request.get_json()
    u_token = params["id"]
    u_id = params["userID"]
    session['token'] = u_token
    session['user'] = u_id
    #return redirect(url_for('question'))
    return jsonify({"userID": session['user'], 'message': 'okay'})


@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('token', None)
    if 'user' in session:
        return jsonify({"message": "error"})

    return jsonify({"message": "okay"})


@app.route('/newsfeed', methods=['GET', 'POST'])
def question():
    url = 'http://iitoverflow.herokuapp.com/api/Questions?filter[include]=answers&filter[include]=tags'

    url2 = 'http://iitoverflow.herokuapp.com/api/Categories'
    response = requests.get(url2)
    categories = response.json()

    url3 = 'http://iitoverflow.herokuapp.com/api/Questions'
    response1 = requests.get(url)
    questions = response1.json()

    # html = urlopen(url).read().decode('utf-8')
    # questions = json.loads(html)
    url1 = 'http://iitoverflow.herokuapp.com/api/Answers'
    html1 = urlopen(url1).read().decode('utf-8')
    answers = json.loads(html1)

    url5 = 'http://iitoverflow.herokuapp.com/api/Tags'
    html5 = urlopen(url5).read().decode('utf-8')
    tag_list = json.loads(html5)

    newlist = []
    for i in tag_list:
        newlist.append(i['name'])

    return render_template('question2.html', tag_list=newlist, questions=questions, answers=answers, categories=categories)

@app.route('/profile', methods=['GET', 'POST'])
def profile2():
    user = str(session['user'])
    url = ('http://iitoverflow.herokuapp.com/api/users/'+user +
           '?filter[include]=questions&filter[include]=interests')
    print(user)
    response = requests.get(url)
    json_object = response.json()

    url = ('http://iitoverflow.herokuapp.com/api/users/'+user +
           '/questionsfollowed?filter={"include":{"relation":"user"}}')
    response = requests.get(url)
    followed_questions = response.json()

    curl = ('http://iitoverflow.herokuapp.com/api/users/'+user +
            '?filter[counts]=followers&filter[counts]=following&filter[counts]=answers&filter[counts]=questionsfollowed&filter[include]=followers&filter[include]=following&filter[include]=answers&filter[include]=questionsfollowed')
    response = requests.get(curl)
    json_object1 = response.json()
    val3 = json_object1['followersCount']
    val4 = json_object1['followingCount']
    val5 = json_object1['answersCount']
    val6 = json_object1['questionsfollowedCount']

    url = ('http://iitoverflow.herokuapp.com/api/users/'+user +
           '/answers?filter[include]=user&filter[include]=question')
    response = requests.get(url)
    answered_questions = response.json()

    return render_template('profile.html', json_object=json_object, json_object1=json_object1, followers=val3, following=val4, followed_questions=followed_questions, answers=val5, questionsfollowed=val6, answered_questions=answered_questions)

@app.route('/profile/<int:id>', methods=['GET', 'POST'])
def profile(id):
    user = str(id)
    url = ('http://iitoverflow.herokuapp.com/api/users/'+user +
           '?filter[include]=questions&filter[include]=interests')
    print(user)
    response = requests.get(url)
    json_object = response.json()

    url = ('http://iitoverflow.herokuapp.com/api/users/'+user +
           '/questionsfollowed?filter={"include":{"relation":"user"}}')
    response = requests.get(url)
    followed_questions = response.json()

    curl = ('http://iitoverflow.herokuapp.com/api/users/'+user +
            '?filter[counts]=followers&filter[counts]=following&filter[counts]=answers&filter[counts]=questionsfollowed&filter[include]=followers&filter[include]=following&filter[include]=answers&filter[include]=questionsfollowed')
    response = requests.get(curl)
    json_object1 = response.json()
    val3 = json_object1['followersCount']
    val4 = json_object1['followingCount']
    val5 = json_object1['answersCount']
    val6 = json_object1['questionsfollowedCount']

    url = ('http://iitoverflow.herokuapp.com/api/users/'+user +
           '/answers?filter[include]=user&filter[include]=question')
    response = requests.get(url)
    answered_questions = response.json()

    return render_template('profile.html', json_object=json_object, json_object1=json_object1, followers=val3, following=val4, followed_questions=followed_questions, answers=val5, questionsfollowed=val6, answered_questions=answered_questions)



@app.after_request
def add_cors(resp):
    resp.headers['Access-Control-Allow-Origin'] = flask.request.headers.get(
        'Origin', '*')
    resp.headers['Access-Control-Allow-Credentials'] = True
    resp.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS, GET, PUT, DELETE'
    resp.headers['Access-Control-Allow-Headers'] = flask.request.headers.get('Access-Control-Request-Headers',
                                                                             'Authorization')
    # set low for debugging

    if app.debug:
        resp.headers["Access-Control-Max-Age"] = '1'
    return resp

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
app.run(debug=True, use_reloader=True, host='0.0.0.0', port=port)
