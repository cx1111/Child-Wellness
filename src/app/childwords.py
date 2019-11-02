from flask import Flask, render_template
app = Flask(__name__)

# Local location of videos
VIDEO_DIR = ''

# Local location of metadata


@app.route('/')
def home():
    return render_template('home.html', key='value')


@app.route('/videos/<video_name>')
def video_detail(video_name):
    """
    Show the video
    """
    return 'Video {}'.format(video_name)


@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id


@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return 'Subpath %s' % escape(subpath)
