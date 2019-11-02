from collections import defaultdict

class WordMetadata:
	"""
	Metadata object to store information about each word in the transcript
	"""
	def __init__(self, start_time, end_time, confidence, word_type):
		self._start_time = start_time
		self._end_time = end_time
		self._confidence = confidence
		self._word_type = word_type

	@property
	def start_time(self):
		return self._start_time

	@start_time.setter
	def start_time(self, time):
		self.start_time = time

	@property
	def end_time(self):
		return self._end_time
	
	@end_time.setter
	def end_time(self, time):
		self._end_time = time

	@property
	def confidence(self):
		return self._confidence 

	@confidence.setter
	def confidence(self, confidence):
		self._confidence = confidence

	@property
	def word_type(self):
		return self._word_type
	
	@word_type.setter
	def word_type(self, word_type):
		self._word_type = word_type

class WordData:
	"""
	Data object to store information about each word in the transcript
	"""
	def __init__(self, content, speaker_id=0, metadata=None):
		self._content = content
		self._speaker_id = speaker_id
		self._metadata = metadata

	@property
	def content(self):
		return self._content
	
	@content.setter
	def content(self, content):
		self._content = content

	@property
	def speaker_id(self):
		return self._speaker_id
	
	@speaker_id.setter
	def speaker_id(self, id):
		self._speaker_id = id

	@property
	def metadata(self):
		return self._metadata

	@metadata.setter
	def metadata(self, metadata):
		self._metadata = metadata

class TranscriptMetadata:
	"""
	Metadata of the transcript such as unique words and cout
	"""
	def __init__(self):
		self._word_histogram = defaultdict(int)

	@property
	def word_histogram(self):
		return self._word_histogram
	
	def add_word(self, word):
		self._word_histogram[word] += 1

class BaseTranscript:
	"""
	Class containing the transcript
	"""
	def __init__(self):
		self._word_list = []
		self._sentence_list = []
		self._metadata = TranscriptMetadata()

		self._current_sentence = []

	@property
	def metadata(self):
		return self._metadata
	
	@property
	def word_list(self):
		return self._word_list

	@property
	def sentence_list(self):
		return self._sentence_list
	
	def add_word(self, word_data):
		"""
		Append word to the end of the transcript

		Pre-conditions:
			word_data.metadata.start_time > self._word_list[-1].metadata.end_time

		Parameters:
			word_data (WordData): WordData object to add to the end of the transcript
		"""
		self._word_list.append(word_data)
		self._metadata.add_word(word_data.content)

		self._current_sentence.append(word_data.content)
		if word_data.content in ['?', '.', '!']:
			self._sentence_list.append(' '.join(self._current_sentence)[:-2] + word_data.content)
			self._current_sentence = []

class SpeakerTranscript(BaseTranscript):
	"""
	Class containing the transcript for a particular speaker
	"""
	def __init__(self, speaker_id):
		super().__init__()
		self._speaker_id = speaker_id

	@property
	def speaker_id(self):
		return self._speaker_id

	@speaker_id.setter
	def speaker_id(self, speaker_id):
		self._speaker_id = speaker_id
	
class MultiSpeakerTranscript(BaseTranscript):
	"""
	Class containing the overall transcript with associated data per word
	as well as seperate transcripts for each speaker
	"""
	def __init__(self):
		super().__init__()
		self._speaker_transcripts = {}
		self._speaker_ids = []

	@property
	def speaker_ids(self):
		return self._speaker_ids
	
	def get_speaker_transcript(self, speaker_id):
		return self._speaker_transcripts[speaker_id]

	def add_word(self, word_data):
		"""
		Append word to the end of the transcript and in the transcript of
		the specific speaker

		Pre-conditions:
			word_data.metadata.start_time > self._word_list[-1].metadata.end_time

		Parameters:
			word_data (WordData): WordData object to add to the end of the transcript
		"""
		super().add_word(word_data)

		speaker_id = word_data.speaker_id
		if speaker_id not in self._speaker_transcripts:
			self._speaker_ids.append(speaker_id)
			self._speaker_transcripts[speaker_id] = SpeakerTranscript(speaker_id)
		self._speaker_transcripts[speaker_id].add_word(word_data)
