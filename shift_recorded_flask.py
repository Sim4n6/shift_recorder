from flask import Flask, url_for, request, render_template
app = Flask(__name__)


@app.route('/')
def hello_world():
    return "Hello world <a href=\"/index\">index</a>"


@app.route('/index')
def index():
    return "well this point to index"


@app.route('/user/<username>')
def print_user(username):
    return f"username is {username}"


@app.route('/id/<int:user_id>')
def get_id(user_id):
    return f'the id is {user_id}'


@app.route('/path/<path:sub_path>')
def get_path(sub_path):
    return f'--> {sub_path} <---'


with app.test_request_context():
    print("url for function get_id with user_id set to 2651651", url_for('get_id', user_id='464654654'))
    print(url_for('get_path', sub_path="/id/5454646/hello/"))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return "a request has been made from client to server : asking to POST some data"
    elif request.method == 'GET':
        return "a request has been made from a client to server : asking to GET something"


@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

