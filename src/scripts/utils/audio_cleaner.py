class AudioCleaner:
    def __init__(self):
        pass

    def clean_audio(self, audio_file):
        self._identify_child_voice(audio_file)
        self._adjust_volume(audio_file)
        self._denoise_background(audio_file)
        self._shift_pitch_down(audio_file)
        self._adjust_sample_rate(audio_file)

    def _shift_pitch_down(self, audio_file):
        pass

    def _identify_child_voice(self, audio_file):
        pass

    def _denoise_background(self, audio_file):
        pass

    def _adjust_volume(self, audio_file):
        pass

    def _adjust_sample_rate(self, audio_file):
        pass
