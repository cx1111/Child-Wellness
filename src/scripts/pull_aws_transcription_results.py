import argparse
import os

from utils import config
from utils.audio_to_text import get_list_of_transcripts, download_transcription
from utils.util import create_dir_if_not_exists

def main(args):
	create_dir_if_not_exists(args.dest_dir)

	for s3_file in get_list_of_transcripts(args.s3_transcription_bucket):
		if s3_file.endswith('.json'):
			s3_file_path = os.path.join(args.s3_transcription_bucket, s3_file)
			print("Downlading file {} to {}".format(s3_file_path, os.path.join(args.dest_dir, s3_file)))
			download_transcription(s3_file_path, args.dest_dir)

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--s3_transcription_bucket', type=str, default=config.BUCKET_TRANSCRIPTION,
						help='name of s3 bucket to fetch output of Transcribe jobs')
	parser.add_argument('--dest_dir', type=str, default='../../data/transcriptions',
						help='output directory to store Transcribe json files')
	args = parser.parse_args()

	main(args)