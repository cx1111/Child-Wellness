import argparse
import pickle
import glob
import os
from datetime import datetime

from utils.aws_transcript_parser import parse_aws_transcript

def get_clip_title(json_file):
	title = os.path.basename(json_file)
	title = title[:title.find('_20')]
	return title

def get_clip_date(json_file):
	timestamp = json_file[json_file.find('_20')+1:json_file.find('.json')]

	date = datetime.strptime(timestamp, '%Y-%m-%d-%H-%M-%S')
	return date.strftime('%m/%d/%Y')

def main(args):
	results = []

	for json_file in sorted(glob.glob(os.path.join(args.json_dir, '*.json'))):
		print("Parsing file {}".format(json_file))
		parsed = parse_aws_transcript(json_file)
		speaker_transcript = parsed.get_speaker_transcript(parsed.speaker_ids[0])
		speaker_unique_words = list(parsed.metadata.word_histogram.keys())
		title = get_clip_title(json_file)
		date = get_clip_date(json_file)

		results.append({
			'title': title,
			'date': date,
			'unique_words': speaker_unique_words,
			'speaker_segments': parsed.speaker_segments
		})

	with open(args.serialized_dest, 'wb') as f:
		pickle.dump(results, f)

	print("Serialized parsed results saved in {}".format(args.serialized_dest))

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--json_dir', type=str, default='../../data/transcriptions',
						help='path to local dir containing transcription json files')
	parser.add_argument('--serialized_dest', type=str, default='../../data/parsed_transcriptions.pkl',
						help='name of s3 bucket to store output of the Transcribe jobs')
	args = parser.parse_args()

	main(args)