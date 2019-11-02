import argparse
import boto3

import config
	
def clear_bucket(bucket_name):
	s3 = boto3.resource('s3')
	bucket = s3.Bucket(bucket_name)
	bucket.objects.all().delete()

def main(args):
	for bucket_name in args.s3_buckets:
		clear_bucket(bucket_name)

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--s3_buckets', type=str, nargs='+',
						default=[config.BUCKET_AUDIO, config.BUCKET_TRANSCRIPTION],
						help='names of s3 bucket to delete')
	args = parser.parse_args()

	main(args)