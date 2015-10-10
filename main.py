from flask import Flask,request,render_template
from google.appengine.ext import ndb
app = Flask(__name__)
app.config['DEBUG'] = True

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

class Poll(ndb.Model):
    content = ndb.StringProperty()
    @classmethod
    def query_poll(cls, ancestor_key):
        return cls.query(ancestor = ancestor_key)

@app.route('/')
@app.route('/topics')
def topics():
    return render_template('topics.html')

@app.route('/poll/<pollname>')
def poll(pollname):
    ancestor_key=ndb.Key("poll",pollname)
    poll=Poll.query_poll(ancestor_key).get()
    if poll is None:
        return "Name your poll, Dummy!", 404
    return pollname + poll.content

@app.route('/results/<pollname>')
def results(pollname):
    return pollname

@app.route('/vote/<pollname>',methods=['POST'])
def vote(pollname):
    return pollname

@app.route('/push/<pollname>',methods=['POST'])
def push(pollname):
    print request.data
    ancestor_key=ndb.Key("poll",pollname)
    poll=Poll.query_poll(ancestor_key).get()
    if poll is None:
        poll=Poll(parent=ancestor_key, content=request.data)
    else:
        poll.content=request.data
    poll.put()
    return request.data

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404

#{
#"question": "Pick a book",
#"pollItems": [
#"book1", "book2", "book3",
#],
#"votes": [
#{
#"voter": "andi",
#"votedItem": [1,0]
#},
#{
#"voter": "katie",
#"votedItem": [0]
#}
#],
#}

#FUNCTIONALITY
#1. space for content/question
#2. ability to add items to poll (by me or by other users)
#3. something clickable to show vote
#4. way to choose/vote for more than one poll item

#CONTENT FOR COMPUTER TO STORE
#1. poll question
#2. poll items + link
#3. votes
