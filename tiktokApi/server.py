import json
import os

from flask import Flask, request

from scraper import scraper

app = Flask(__name__)


@app.route('/users_from_ready_csv/<csv_file_name>')
def user_query_from_csv(csv_file_name):
    output = scraper.get_from_csv(csv_file_name)
    return json.dumps(output)


@app.route('/user/<username>')
def user_query(username):
    num_posts = request.args.get('num_posts', default=0, type=int)
    since=request.args.get('since', default=0, type=int)
    before=request.args.get('before', default=0, type=int)


    output = scraper.scrap_users([username], num_posts, since, before)[0]
    #

    print("Sdasdasd")
    return json.dumps(output)


@app.route('/music/<music_id>')
def music_query(music_id):
    num_posts = request.args.get('num_posts', default=0, type=int)
    since=request.args.get('since', default=0, type=int)
    before=request.args.get('before', default=0, type=int)

    output = scraper.scrap_musics([music_id], num_posts, since, before)
    return json.dumps(output)


@app.route('/hashtag/<hashtag>')
def hashtag_query(hashtag):
    num_posts = request.args.get('num_posts', default=0, type=int)
    since=request.args.get('since', default=0, type=int)
    before=request.args.get('before', default=0, type=int)

    output = scraper.scrap_hashtags([hashtag], num_posts, since, before)
    return json.dumps(output)


@app.route('/post/<username>/<post_id>')
def post_query(username, post_id):
    output = scraper.scrap_posts([username], [post_id])
    return output


def get_lines_of_uploaded_file(filename):
    file = request.files[filename]
    file.save('temp')
    with open('temp', encoding='utf8') as file:
        lines = [line.strip() for line in file]
    os.remove('temp')
    return lines


@app.route('/users', methods=['POST'])
def users_query():
    usernames = get_lines_of_uploaded_file('usernames')
    num_posts = request.values.get('num_posts', default=0, type=int)
    since=request.args.get('since', default=0, type=int)
    before=request.args.get('before', default=0, type=int)

    output = scraper.scrap_users(usernames, num_posts, since, before)
    return json.dumps(output)


@app.route('/musics', methods=['POST'])
def musics_query():
    music_ids = get_lines_of_uploaded_file('music_ids')
    num_posts = request.values.get('num_posts', default=0, type=int)
    since=request.args.get('since', default=0, type=int)
    before=request.args.get('before', default=0, type=int)

    output = scraper.scrap_musics(music_ids, num_posts, since, before)
    return json.dumps(output)


@app.route('/hashtags', methods=['POST'])
def hashtags_query():
    hashtags = get_lines_of_uploaded_file('hashtags')
    num_posts = request.values.get('num_posts', default=0, type=int)

    output = scraper.scrap_hashtags(hashtags, num_posts)
    return json.dumps(output)


@app.route('/posts', methods=['POST'])
def posts_query():
    posts = get_lines_of_uploaded_file('posts')
    usernames, post_ids = zip(*[post.split(',') for post in posts])

    output = scraper.scrap_posts(usernames, post_ids)
    return output


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=4555)
