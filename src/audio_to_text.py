import boto3
import os


def transcribe_audio(audio_uri,output_bucket):


    client = boto3.client('transcribe')

    file_name = os.path.basename()


    response = client.start_transcription_job(
        TranscriptionJobName=file_name,
        LanguageCode='en-US'|'es-US'|'en-AU'|'fr-CA'|'en-GB'|'de-DE'|'pt-BR'|'fr-FR'|'it-IT'|'ko-KR'|'es-ES'|'en-IN'|'hi-IN'|'ar-SA'|'ru-RU'|'zh-CN',
        MediaSampleRateHertz=123,
        MediaFormat='mp3'|'mp4'|'wav'|'flac',
        Media={
            'MediaFileUri': audio_uri
        },
        OutputBucketName=output_bucket,
        OutputEncryptionKMSKeyId='string',
        Settings={
            'VocabularyName': 'string',
            'ShowSpeakerLabels': True,
            'MaxSpeakerLabels': 10,
            'ChannelIdentification': False
        }
    )

    return response

