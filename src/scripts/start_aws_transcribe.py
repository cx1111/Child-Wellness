import argparse
import tempfile
import shutil
import glob
import os

from utils import config
from utils.video_to_audio import convert_videos_in_dir
from utils.audio_cleaner import AudioCleaner
from utils.audio_to_text import upload_audio_in_dir, transcribe_audio
from utils.audio_to_text import get_list_of_audio_files

def transcribe_audio_s3(s3_audio_bucket, s3_transcription_bucket):
	s3_uri = 'https://{}.s3-us-west-1.amazonaws.com'.format(config.BUCKET_AUDIO)
	s3_audio_files = get_list_of_audio_files(s3_audio_bucket)
	for s3_file in s3_audio_files:
		s3_file_uri = os.path.join(s3_uri,s3_file)
		print("Starting Transcribe job for {}".format(s3_file_uri))
		transcribe_audio(s3_file_uri, s3_transcription_bucket)

def preprocess_audio_files(audio_dir):
	audio_cleaner = AudioCleaner()

	for audio_file in glob.glob(os.path.join(audio_dir, "*")):
		audio_cleaner.clean_audio(audio_file)

def convert_videos_to_audio(video_dir):
	dest_dir = tempfile.mkdtemp()
	convert_videos_in_dir(video_dir, dest_dir)
	return dest_dir

def main(args):
	if args.src_video_dir:
		# Convert all videos to audio files and store in temp dir
		audio_dir = convert_videos_to_audio(args.src_video_dir)
	elif args.src_audio_dir:
		# Skip the video to audio conversion step
		audio_dir = args.src_audio_dir

	# Preprocess audio files before uploading
	preprocess_audio_files(audio_dir)
	# Upload to S3
	upload_audio_in_dir(audio_dir, args.s3_audio_bucket)
	# Start transcription jobs
	transcribe_audio_s3(args.s3_audio_bucket, args.s3_transcription_bucket)

	if args.src_video_dir:
		# Remove temp audio dir
		shutil.rmtree(audio_dir)
	
if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	group = parser.add_mutually_exclusive_group(required=True)
	group.add_argument('--src_video_dir', type=str, default=None,
						help='directory containing videos to transcribe')
	group.add_argument('--src_audio_dir', type=str, default=None,
						help='directory containing audio to transcribe')
	parser.add_argument('--s3_audio_bucket', type=str, default=config.BUCKET_AUDIO,
						help='name of the s3 bucket to store audio for the Transcribe jobs')
	parser.add_argument('--s3_transcription_bucket', type=str, default=config.BUCKET_TRANSCRIPTION,
						help='name of s3 bucket to store output of the Transcribe jobs')
	args = parser.parse_args()

	main(args)