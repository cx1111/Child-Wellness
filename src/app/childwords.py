from . import benchmark
from . import vocabloader
from datetime import datetime
import os

from flask import Flask, render_template, request
app = Flask(__name__)


# Local location of videos
VIDEO_DIR = os.path.join(app.root_path, 'static', 'videos')

# Local location of metadata

CHILD = {
    'name': 'Alexandria',
    'dob': '31/06/2017',
}


@app.route('/')
def dashboard():
    "The upper home landing page with all apps shown"
    child = CHILD.copy()
    child['age'] = '32 month'
    return render_template('dashboard.html', child=child)


@app.route('/vocabulary')
def vocabulary():
    """
    The vocabulary home page. Contains graphs and headline figures

    Graphs:
    - Line graph of cumulative word count
    - Line graph of average syllable count
    -

    Headline Figures:
    - Total unique words in lifetime
    - Wordcount percentile
    - Recent average syllable count
    - Syllable percentile
    - Longest word
    - Whether they are getting into Stanford

    """
    # Load NIH benchmarks and distributions

    # Load metadata from all videos, ordered by datetime
    child_transcripts = vocabloader.get_child_transcripts()
    cumulative_stats = vocabloader.get_cumulative_stats(child_transcripts)

    headline_figures = {
        'wordcount': 270, 'wordcount_percentile': 88,
        'average_syllables': 2.8, 'syllable_percentile': 96,
        'longest_word': 'Miscellaneous', 'favorite_word': 'Chicken',
        'getting_into_stanford': False}

    child = CHILD.copy()
    child['age'] = '32 month'

    return render_template(
        'home.html', child=child, headline_figures=headline_figures,
        cumulative_wordcount=cumulative_stats,
        average_wordcount=benchmark.AVERAGE_WORDCOUNT,
        average_syllables=benchmark.AVERAGE_SYLLABLES,)


@app.route('/videos/<video_name>')
def video_detail(video_name):
    """
    Show the video and associated detail
    """
    transcript = vocabloader.get_transcript('ExampleReal')
    speaker_segments = transcript['speaker_segments']

    # Hardcode url for now
    video_info = {
        'title': video_name,
        'url': 'https://drive.google.com/file/d/11dRucTxdfx6Soy_ldkzSaiDJ1I2eSV72/preview',
        'transcript': speaker_segments}
    return render_template('video_detail.html', video_info=video_info)
