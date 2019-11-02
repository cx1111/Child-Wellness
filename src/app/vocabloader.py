def get_child_transcripts():
    """
    Get all transcripts in date asc order with following info for each
    vid/transcript:
    - vid title
    - date
    - list of unique words
    - Video file path

    """
    # Replace this with real db/data file loading
    child_transcripts = child_transcripts = [
        {'title': 'Video 1', 'date': '11/09/2017',
         'unique_words': ['hi', 'dada', 'mama', 'haha', 'no'],
         'file_path': ''},
        {'title': 'Video 2', 'date': '01/12/2017',
         'unique_words': ['hi', 'dada', 'mama', 'haha', 'no'],
         'file_path': ''},
        {'title': 'Video 3', 'date': '25/02/2018',
         'unique_words': ['hi', 'dada', 'mama', 'haha', 'no'],
         'file_path': ''}]

    return child_transcripts


def get_cumulative_stats(child_transcripts):
    """
    From a list of child transcripts, get cumulative stats for each date
    (keeping the order of inputs). Stats required:

    - Running wordcount
    -
    """

    cumulative_stats = []
    all_words = set()
    for t in child_transcripts:
        # Cumulative words
        all_words = all_words = all_words.union(set(t['unique_words']))
        # Copy over common fields
        stats = {key: t[key] for key in ('title', 'date', 'file_path')}
        # Add cumulative stats
        stats['wordcount'] = len(all_words)
        cumulative_stats.append(stats)

    return cumulative_stats
