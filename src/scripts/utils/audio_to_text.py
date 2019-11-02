import boto3
import os
from datetime import datetime
from . import config
import glob

def transcribe_audio(audio_uri, output_bucket=config.BUCKET_TRANSCRIPTION):
    """
    Convert the given audio file to an transcription file in the specified s3 bucket

    Parameters:
        audio_uri (str): Source audio file s3 uri to be converted
        output_bucket (str): Destination for the transcription json file
    """
    client = boto3.client('transcribe')

    file_name = os.path.basename(audio_uri).split('.')[0] + '_' + datetime.now().strftime('%Y%m%d%H%m%s')
    file_format = os.path.basename(audio_uri).split('.')[1]

    output_path = output_bucket + '/' + file_name + '.json'

    response = client.start_transcription_job(
        TranscriptionJobName=file_name,
        LanguageCode='en-US',
        MediaFormat=file_format,
        Media={
            'MediaFileUri': audio_uri
        },
        OutputBucketName=output_bucket,

        Settings={
            'ShowSpeakerLabels': True,
            'MaxSpeakerLabels': 10,
            'ChannelIdentification': False
        }
    )

    if response['TranscriptionJob']['TranscriptionJobStatus'] == 'IN_PROGRESS':
        return output_path, response
    return 'something went wrong'


def upload_audio_in_dir(dir_path, bucket=config.BUCKET_AUDIO):
    """
    Uploads all files in the given directory to the target s3 bucket

    Parameters:
        dir_path (str): Source dir where audio files are to be uploaded
        bucket (str): Destination for the uploaded file
    """
    for file_path in glob.glob(os.path.join(dir_path, "*")):
        print("Uploading file {}".format(file_path))
        result = upload_audio(file_path)

def upload_audio(file_path,bucket=config.BUCKET_AUDIO):
    """
    Uploads a file to the target s3 bucket

    Parameters:
        file_path (str): Source file to be uploaded
        bucket (str): Destination for the uploaded file
    """
    file_name = os.path.basename(file_path)

    s3 = boto3.client('s3')

    with open(file_path, 'rb') as data:
        response = s3.upload_fileobj(data, bucket, file_name)

    return response


def download_transcription(input_path,output_folder):
    """
    Uploads downloads a file from s3 and saves to target location

    Parameters:
        input_path (str): s3 file to be downloaded in <bucket_name>/<file_name> format
        output_folder (str): target folder where file will be saved
    """
    file_name = input_path.split('/')[1]
    bucket = input_path.split('/')[0]
    download_target = os.path.join(output_folder,file_name)

    s3 = boto3.resource('s3')

    s3.meta.client.download_file(bucket, file_name, download_target)

def get_list_of_audio_files(bucket=config.BUCKET_AUDIO):
    s3 = boto3.client('s3')

    response = s3.list_objects(
        Bucket=bucket,
    )
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        transcripts_file_lists = [i['Key'] for i in response['Contents']]

    return transcripts_file_lists

def get_list_of_transcripts(bucket=config.BUCKET_TRANSCRIPTION):
    s3 = boto3.client('s3')

    response = s3.list_objects(
        Bucket=config.BUCKET_TRANSCRIPTION,
    )
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        transcripts_file_lists = [i['Key'] for i in response['Contents']]

    return transcripts_file_lists

