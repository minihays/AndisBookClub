from flask import Flask,request,render_template
from google.appengine.ext import ndb
app = Flask(__name__)
app.config['DEBUG'] = True

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

class Greeting(ndb.Model):
    content = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add = True)

    @classmethod
    def query_book(cls, ancestor_key):
        return cls.query(ancestor = ancestor_key).order(-cls.date)

@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello World!'

@app.route('/bye')
def bye():
    """Return a friendly HTTP greeting."""
    return 'See Ya World!'

@app.route('/submit')
def submit():
    guestbookname = request.args.get('guestbook_name')
    greeting = Greeting(parent = ndb.Key("Book", guestbookname or "NoTitle"), content = request.args.get('content'))
    greeting.put()
    return 'Saved'

@app.route('/greetings')
def greetings():
    guestbookname = request.args.get('guestbook_name')
    ancestor_key = ndb.Key("Book", guestbookname or "NoTitle")
    greetings = Greeting.query_book(ancestor_key).fetch(20)
    output = ''
    for greeting in greetings:
        output += greeting.content + " xxx "
    return output

@app.route('/topics')
def topics():
    return render_template('topics.html')




@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
