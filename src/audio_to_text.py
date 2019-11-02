import boto3
import os
from datetime import datetime

def transcribe_audio(audio_uri,output_bucket):


    client = boto3.client('transcribe')


    file_name = os.path.basename(audio_uri).split('.')[0] + datetime.now().strftime('%Y%m%d%H%m')
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
            # 'VocabularyName': 'string',
            'ShowSpeakerLabels': True,
            'MaxSpeakerLabels': 10,
            'ChannelIdentification': False
        }
    )

    return output_path, response


input_file = 'https://dvhacksaudioinput.s3-us-west-1.amazonaws.com/kids1.mp3'
output_bucket = 'dvhacksout'
result = transcribe_audio(input_file,output_bucket)
print(result)