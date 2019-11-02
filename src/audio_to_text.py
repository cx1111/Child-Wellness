import boto3
import os
from datetime import datetime


def transcribe_audio(audio_uri, output_bucket):
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

