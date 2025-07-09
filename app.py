from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from utils import checkThread, checkComment
from flask_cors import CORS
from models import db, Thread, Comment

app = Flask(__name__)

# Configure database
app.config['SECRET_KEY'] = 'secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Enable CORS
CORS(app)

# Initialize db to be used with current Flask app
with app.app_context():
    db.init_app(app)

    db.create_all()

@app.route('/')
def home():
    threads = Thread.query.order_by(Thread.upvotes.desc()).all() #sorts by upvotes
    return render_template('home.html', threads=threads) # return list of threads


@app.route('/thread/<int:thread_id>')
def thread(thread_id):
    thread = Thread.query.get_or_404(thread_id) # returns a 404 error if get fails
    print(thread)
    return render_template('thread.html', thread=thread) # return the thread object

@app.route('/new_thread', methods=['POST'])
def new_thread():
    form = request.get_json()
    title = form["title"]
    content = form["content"]
    author = form.get("author")

    if not title or not content or not author:
        return jsonify({"success": "false", "error": "Missing required fields"}), 400  #return JSON instead of HTML!

    if not checkThread(title, content, author):
        return jsonify({"success": "false", "error": "Content violates moderation rules"}), 400  #same here

    else:
        new_thread = Thread(title=title, content=content, author=author)
        db.session.add(new_thread)
        db.session.commit()
        print(f"Added new thread: {new_thread.serialize()}")
        return make_response(jsonify({"success": "true", "thread": new_thread.serialize()}), 200) 
        # return both JSON object and HTTP response status (200: OK)

    return make_response(jsonify({"success": "false"}), 400) # return both JSON object and HTTP response status (400: bad request)

@app.route('/comment/<int:thread_id>', methods=['POST'])
def comment(thread_id):
    thread = Thread.query.get_or_404(thread_id) # return 404 error if get fails
    form = request.get_json()
    comment_text = form.get("content")
    author = form.get("author")

    if not comment_text or not author:
        return jsonify({"success": "false", "error": "Missing required fields"}), 400

    if not checkComment(comment_text, author):
        return jsonify({"success": "false", "error": "Comment violates moderation rules"}), 400
    else:
        new_comment = Comment(thread_id=thread.id, content=comment_text, author=author)
        db.session.add(new_comment)
        db.session.commit()

    # error = False
    # if error:
    #     return redirect(url_for('error'))
    #return redirect(url_for('thread', thread_id=thread_id)) # set variable thread_id to be thread_id
     # Return JSON with the new comment
    
    return jsonify({"success": "True", "comment": {"author": author,"content": comment_text}}), 200

   
# @app.route('/upvote/<int:thread_id>', methods=['PUT'])
# def upvote_thread(thread_id):
#     """Handles upvoting a thread."""
#     thread = Thread.query.get_or_404(thread_id)  # Get thread or return 404
#     thread.upvotes += 1  # increment upvote count
#     db.session.commit()

#     return jsonify({"success": True, "upvotes": thread.upvotes}), 200  #now we return updated upvote count


@app.route('/vote/<int:thread_id>', methods=['PUT'])
def vote_thread(thread_id):
    """Handles both upvotes and downvotes for a thread."""
    thread = Thread.query.get_or_404(thread_id)
    data = request.get_json()

    if data["vote"] == "upvote":
        thread.upvotes += 1  # Increase upvotes
    elif data["vote"] == "downvote":
        thread.upvotes -= 1  # Decrease upvotes (can be negative)

    db.session.commit()

    return jsonify({"success": True, "upvotes": thread.upvotes}), 200


@app.route('/error')
def errorPage():
    # tells the user that a particular author has posted too much
    # page should extend a "base.html" HTML template that includes a header, footer, and navigation bar
    return render_template('error.html', message="This author has poster too much."), 404

if __name__ == '__main__':
    app.run(debug=True)