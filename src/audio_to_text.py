import boto3
import os
from datetime import datetime
import config


def transcribe_audio(audio_uri, output_bucket=config.BUCKET_TRANSCRIPTION):
    client = boto3.client('transcribe')

    file_name = os.path.basename(audio_uri).split('.')[0] + datetime.now().strftime('%Y%m%d%H%m%s')
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


def upload_audio(file_path,bucket=config.BUCKET_AUDIO):

    file_name = os.path.basename(file_path)

    s3 = boto3.client('s3')

    with open(file_path, 'rb') as data:
        response = s3.upload_fileobj(data, bucket, file_name)

    return response


def download_transcription(input_path,output_folder):
    file_name = input_path.split('/')[1]
    bucket = input_path.split('/')[0]
    download_target = os.path.join(output_folder,file_name)

    s3 = boto3.resource('s3')

    s3.meta.client.download_file(bucket, file_name, download_target)
