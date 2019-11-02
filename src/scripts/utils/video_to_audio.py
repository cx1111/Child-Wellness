import argparse
import glob
import os
import moviepy.editor as mp

from .util import *

def convert_video(video_file, dest_audio_file):
	"""
	Convert the given video file to an audio file in the specified location

	Parameters:
		video_file (str): Source video file to be converted
		dest_audio_file (str): Destination for the converted audio file
	"""

	video = mp.VideoFileClip(video_file)
	video.audio.write_audiofile(dest_audio_file)

def get_dest_audio_file(video_file, dest_dir, dest_ext):
	"""
	Create the destination path for the converted audio file

	Parameters:
		video_file (str): Source video file to be converted
		video_ext (str): Extension type of the video
		dest_dir (str): Destination directory to store the audio
		dest_ext (str): Extension that the audio file will be converted to
	"""
	video_basename = os.path.basename(video_file)
	_, video_ext = os.path.splitext(video_basename)
	audio_basename = video_basename.replace(video_ext, dest_ext)
	return os.path.join(dest_dir, audio_basename)

def convert_videos_in_dir(video_dir, dest_dir, 
						  video_ext=['.mp4', '.mov', '.ogv', '.mpeg', '.avi'],
						  dest_ext='.mp3'):
	"""
	Convert all videos in the given directory of the specified type to audio files
	that will be stored in the provided directory

	Parameters:
		video_file (str): Source video file to be converted
		dest_dir (str): Destination directory to store the audio
		video_ext (str): Extension type of the video
		dest_ext (str): Extension that the audio file will be converted to
	"""

	# Ensure that dest dir exists
	create_dir_if_not_exists(dest_dir)

	# Gather all video files to convert
	video_files = []
	for ext in video_ext:
		video_files += glob.glob(os.path.join(video_dir, "*{}".format(ext)))

	# Convert video files in the dir to audio files in the dest dir
	for video_file in video_files:
		dest_audio_file = get_dest_audio_file(video_file, dest_dir, dest_ext)
		convert_video(video_file, dest_audio_file)

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('video_dir', type=str, 
						help='directory containing videos to convert to audio')
	parser.add_argument('dest_dir', type=str,
						help='directory to store converted audio files')
	parser.add_argument('--video_ext', type=str, nargs='+',
						default=['.mp4', '.mov', '.ogv', '.mpeg', '.avi'],
						help='extensions of video files to convert')
	parser.add_argument('--dest_ext', type=str, default='.mp3',
						help='extension audio files will be converted to')
	args = parser.parse_args()
	
	convert_videos_in_dir(args.video_dir, args.dest_dir,
						  args.video_ext, args.dest_ext)
