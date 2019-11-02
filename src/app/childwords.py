import os

from flask import Flask, render_template, request
app = Flask(__name__)

# Local location of videos
VIDEO_DIR = os.path.join(app.root_path, 'static', 'videos')

# Local location of metadata


@app.route('/')
def home():
    return render_template('home.html', key='value')


@app.route('/videos/<video_name>')
def video_detail(video_name):
    """
    Show the video and associated detail
    """
    return 'Video {}'.format(video_name)


@app.route('/realhome')
def real_home():
    "Upper landing page with all apps shown"
    return 'I wonder if we will get to this'
