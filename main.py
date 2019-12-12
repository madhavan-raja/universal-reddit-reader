from flask import Flask, render_template, request, url_for
import praw
import json
import random
import markdown2

creds = json.load(open("credentials.json"))

subs = [
    'nosleep',
    'ProRevenge',
    'NuclearRevenge'
]

LIMIT = 100

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', subs=subs)

@app.route('/<sub_name>')
def display_post(sub_name):
    reddit = praw.Reddit(client_id=creds['client_id'], client_secret=creds['client_secret'], username=creds['username'], password=creds['password'], user_agent=creds['user_agent'])

    try:
        sub = reddit.subreddit(sub_name)
        sub_hot = sub.hot(limit=LIMIT)
        random_post = random.choice(list(sub_hot))
    except:
        return render_template('error.html')

    body_text = random_post.selftext
    body = markdown2.markdown(random_post.selftext)

    return render_template("display_post.html", sub=random_post.subreddit.display_name, author=random_post.author.name, title=random_post.title, url=random_post.url, upvote_ratio=int(random_post.upvote_ratio * 100), body=body, body_text=body_text)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)