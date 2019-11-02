def get_child_transcripts():
    """
    Get all transcripts in date asc order with following info for each
    vid/transcript:
    - vid title
    - date
    - list of unique words
    - Video file path

    """

    fake_ages = {
        'Example1': 16, 'Example2': 18, 'Example3': 20, 'Example4': 22,
        'Example5': 24, 'Example6': 26, 'Example7': 27, 'Example8': 28,
        'Example9': 30, 'ExampleReal': 32, }

    # Replace this with real db/data file loading
    child_transcripts = child_transcripts = [
        {'title': 'Example1', 'date': '11/09/2017',
         'unique_words': ['hi', 'dada', 'mama', 'haha', 'no'],
         'file_path': ''},
        {'title': 'Example2', 'date': '01/12/2017',
         'unique_words': ['hi', 'dada', 'mama', 'haha', 'no'],
         'file_path': ''},
        {'title': 'Example3', 'date': '25/02/2018',
         'unique_words': ['hi', 'dada', 'mama', 'haha', 'no'],
         'file_path': ''}]

    for i in child_transcripts:
        i['age_months'] = fake_ages[i['title']]

    return child_transcripts


def get_cumulative_stats(child_transcripts):
    """
    From a list of child transcripts, get cumulative stats for each date
    (keeping the order of inputs). Stats required:

    - Running wordcount
    - Others tbd....
    """

    cumulative_stats = []
    all_words = set()
    for t in child_transcripts:
        # Cumulative words
        all_words = all_words = all_words.union(set(t['unique_words']))
        # Copy over common fields
        stats = {key: t[key]
                 for key in ('title', 'date', 'file_path', 'age_months')}
        # Add cumulative stats
        stats['wordcount'] = len(all_words)
        cumulative_stats.append(stats)

    return cumulative_stats
