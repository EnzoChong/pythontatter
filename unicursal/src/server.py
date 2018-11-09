# -*- coding=utf8 -*-

from flask import Flask, request, Response
import time
import random
import soloution
import default_conf as conf

app = Flask(__name__, static_url_path = conf.wwwroot)

result_page = """
<img src="image/{}" alt="result">
"""

@app.route('/index.html', methods = ['GET'])
@app.route('/main.html', methods = ['GET'])
@app.route('/upload', methods = ['GET'])
@app.route('/', methods = ['GET'])
def main_page():
    print request.args
    with open(conf.wwwroot + '/index.html') as f:
        page = f.read()
    return page

@app.route('/upload', methods = ['POST'])
def post_form():
    filename = str(int(time.time())) + '.PNG'
    path = conf.wwwroot + '/image/' + filename
    filedata = request.files.get('image')
    filedata.save(path)
    
    s = soloution.Soloution(path)
    s.analyse()

    answer_image = s.draw_answer()
    if answer_image is not None:
        return result_page.format(answer_image)
    else:
        return "error answer"

@app.route('/first.html', methods = ['GET'])
def test_page1():
    get_page = """
    <html>
        <head>
        <title>Hello world!</title>
        </head>
        <body>
        <p>Hello world!</p>
        </body>
    </html>
    """
    return get_page

@app.route('/second.html', methods = ['GET'])
def test_page2():
    post_page = """
    <html>
        <head>
            <title>Enter your info</title>
        </head>
        <body>
            <form action="/post.html" method="post">
            <input type="text" name="name" id="name">
            <input type="text" name="pwd" id="pwd">
            <input type="submit" name="submit" id="submit">
            </form>
        </body>
    </html>
    """
    return post_page

@app.route('/post.html', methods = ['POST'])
def test_page3():
    page = """
    <html>
        <head>
            <title>Your info</title>
        </head>
        <body>
            <p>YourName:{}</p>
            <br>
            <p>YourPasswd:{}</p>
        </body>
    </html>
    """
    name = request.form['name']
    passwd = request.form['pwd']
    return page.format(name, passwd)

@app.route('/image/<int:imageid>', methods = ['GET'])
def image_back(imageid):
    image = file(conf.wwwroot + "/image/{}.PNG".format(imageid))
    resp = Response(image, mimetype="image/jpeg")
    return resp

if __name__ == '__main__':
    app.run()
