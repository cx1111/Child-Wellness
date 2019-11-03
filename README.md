# Predictive Child Wellness

## About

{app_name} leverages the photos and videos taken by users of their children to benchmark their child's development and identify disease indications.
 

## Usage

### Installation and Setup

#### Python

Install Python 3.7.

Install Python requirements:
```
pip install -r requirements.txt
```

#### AWS Credentials

AWS is a key part of {app_name} and is required in order to run the entire pipeline. Credentials should be stored in `~/.aws/credentials` in the following format

```
[{app-name}]
aws_access_key_id = <access-key-id>
aws_secret_access_key = <secret-access-key>
```

### Transcribing video/audio clips

#### Amazon Transcribe

{app_name} leverages [Amazon Transcribe](https://aws.amazon.com/transcribe/) to perform automatic speech recognition (ASR) and partitioning of audio into homogeneous segments according to the speaker identity. Given an audio clip, Amazon Transcribe will produce json files similar to the one below:

```
{
  "jobName": "job ID",
  "accountId": "account ID",
  "results": {
    "transcripts": [
      {
        "transcript": "Professional answer."
      }
    ],
    "speaker_labels": {
      "speakers": 1,
      "segments": [
        {
          "start_time": "0.000000",
          "speaker_label": "spk_0",
          "end_time": "1.430",
          "items": [
            {
              "start_time": "0.100",
              "speaker_label": "spk_0",
              "end_time": "0.690"
            },
            {
              "start_time": "0.690",
              "speaker_label": "spk_0",
              "end_time": "1.210"
            }
          ]
        }
      ]
    },
    "items": [
      {
        "start_time": "0.100",
        "end_time": "0.690",
        "alternatives": [
          {
            "confidence": "0.8162",
            "content": "Professional"
          }
        ],
        "type": "pronunciation"
      },
      {
        "start_time": "0.690",
        "end_time": "1.210",
        "alternatives": [
          {
            "confidence": "0.9939",
            "content": "answer"
          }
        ],
        "type": "pronunciation"
      },
      {
        "alternatives": [
          {
            "content": "."
          }
        ],
        "type": "punctuation"
      }
    ]
  },
  "status": "COMPLETED"
}
``` 

#### Starting Amazon Transcribe jobs on your videos/audio

In order to start transcribing videos/audio stored locally on your machine using Amazon Transcribe, run the following:

```
cd src/scripts/
python start_aws_transcribe.py --src_video_dir=/path/to/dir/with/videos
```

Note that `--src_audio_dir` can be specified instead if you wish to transcribe audio clips. Please reference `python start_aws_transcribe.py --help` for more options such as S3 bucket names.

### Getting Transcripts from Amazon Transcribe

Transcriptions are stored as `json` objects in an S3 bucket upon completion of a job. Once all jobs are completed, the following will pull them down to be stored locally

```
python pull_aws_transcription_results.py 
```

By default, these transcripts will be stored in `../../data/transcriptions` but can be changed by using `--dest_dir`. Please reference `python pull_aws_transcription_results.py --help` for more options.

### Processing Amazon Transcribe Outputs

Once these json transcripts are pulled down locally, they can be processed and serialized into a format that is expected by the frontend.

```
python parse_aws_transcription_results.py
```

For more options on specifying the input directory and destination `.pkl` file, please reference `python parse_aws_transcription_results.py --help`.

### Running the Web Application

Run the main Flask app:
```
cd src/app
FLASK_APP=childwords.py flask run
```
