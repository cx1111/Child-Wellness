


class AudioCleaner:

    def __init__(self):
        pass

    def clean_audio(self,audio_file):
        self.audio_file = audio_file

        self.identify_child_voice()
        self.adjust_volume()
        self.denoise_background()
        self.shift_pitch_down()
        self.adjust_sample_rate()

    def shift_pitch_down(self):
        pass

    def identify_child_voice(self):
        pass

    def denoise_background(self):
        pass

    def adjust_volume(self):
        pass

    def adjust_sample_rate(self):
        pass
