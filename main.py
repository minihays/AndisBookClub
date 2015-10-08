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
@app.route('/topics')
def topics():
    return render_template('topics.html')




@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
