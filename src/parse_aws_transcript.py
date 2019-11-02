import argparse
import json

from transcript import *

parser = argparse.ArgumentParser()
parser.add_argument('json_transcript', type=str, 
					help='path to transcript json file to parse')
args = parser.parse_args()

def get_punct_data(word_segment, time, speaker_id):
	"""
	Create a WordData object from the parsed word_segment json object
	that contains punctuation

	Parameters:
		word_segment (str): json object with data on the punctuation
		time (str): start and end time of the punctuation
		speaker_id (str): speaker of the punctuation

	Returns:
		word_data (WordData): object with details of the punctuation
	"""
	word_metadata = WordMetadata(
		start_time=time,
		end_time=time,
		confidence=word_segment['alternatives'][0]['confidence'],
		word_type=word_segment['type']
	)

	return WordData(
		content=word_segment['alternatives'][0]['content'],
		speaker_id=speaker_id,
		metadata=word_metadata
	)

def get_word_data(word_segment, speaker_id):
	"""
	Create a WordData object from the parsed word_segment json object
	that contains spoken word info

	Parameters:
		word_segment (str): json object with data on the word
		speaker_id (str): speaker of the word

	Returns:
		word_data (WordData): object with details of the word
	"""
	word_metadata = WordMetadata(
		start_time=word_segment['start_time'],
		end_time=word_segment['end_time'],
		confidence=word_segment['alternatives'][0]['confidence'],
		word_type=word_segment['type']
	)

	return WordData(
		content=word_segment['alternatives'][0]['content'],
		speaker_id=speaker_id,
		metadata=word_metadata
	)

def parse_aws_transcript(json_file):
	"""
	Parse an AWS json transcript file into a MultiSpeakerTranscript object

	Parameters:
		json_file (str): path to json file to parse

	Returns:
		transcript (MultiSpeakerTranscript): object with all spoken words labeled
			and split for each speaker with associated metadata
	"""
	with open(json_file, 'r') as f:
		data = json.load(f)

	# Map speaking start times to speaker id
	speaker_start_times = {}
	labels = data['results']['speaker_labels']['segments']
	for label in labels:
		items = label['items']
		for item in items:
			speaker_start_times[item['start_time']] = label['speaker_label']


	# Associate words with speakers and metadata and build transcript object
	last_end_time = 0
	last_speaker_id = 0
	transcript = MultiSpeakerTranscript()
	word_segments = data['results']['items']
	for word_segment in word_segments:
		if 'end_time' in word_segment:
			# Extract details about the word
			speaker_id = speaker_start_times[word_segment['start_time']]
			word_data = get_word_data(word_segment, speaker_id)

			# Record last time and speaker
			last_end_time = word_segment['end_time']
			last_speaker_id = speaker_id
		else:
			# Punctuation doesn't have start and end times so use the latest time
			word_data = get_punct_data(word_segment, last_end_time, last_speaker_id)

		# Add word to transcript
		transcript.add_word(word_data)

	return transcript

if __name__ == '__main__':
	parse_aws_transcript(args.json_transcript)