import cmudict
import string


class TextAnalyzer:
    def __init__(self,lang='en'):
        if lang == 'en':
            self.cmu_dict = cmudict.dict()


    def count_syllables_word(self,word):
        """
        Counts the approximate the number of syllables in a word

        Parameters:
            word (str): s3 file to be downloaded in <bucket_name>/<file_name> format

        Returns:
            syl_count (int): the approximate the number of syllables in a word

        Notes:
            This is a particularly difficult problem which is not completely solved by the LaTeX hyphenation algorithm.
            A good summary of some available methods and the challenges involved can be found in the paper
            Evaluating Automatic Syllabification Algorithms for English (Marchand, Adsett, and Damper 2007).

            Only works for North American English
        """

        try:
            syl_count = [len(list(y for y in x if y[-1].isdigit())) for x in self.cmu_dict[word.lower()]]
            return syl_count[0]
        # Try/Except included because word might not be included in the cmu dictionary
        except:
            return 0



    def count_syllables_sentence(self,sent):
        """
        Counts the approximate the number of syllables in a sentance

        Parameters:
            word (str): s3 file to be downloaded in <bucket_name>/<file_name> format

        Returns:
            syl_count (int): the approximate the number of syllables in a word


        """
        syl_count = 0

        assert type(sent) == str,'sentance should be a string'
        sent = sent.translate(str.maketrans('', '', string.punctuation))
        sent = " ".join(sent.split())
        sent = sent.split(' ')

        for word in sent:
            print(word)
            syl_count += self.count_syllables_word(word)

        return syl_count

    def count_words_sentence(self, sent):
        if type(sent) == str:
            sent = sent.translate(str.maketrans('', '', string.punctuation))
            sent = " ".join(sent.split())
            sent = sent.split(' ')

        return len(sent)

    def test_algos(self):
        self.test_count_syllables_word()
        self.test_count_syllables_sentence()
        self.test_count_words_sentence()

    def test_count_syllables_word(self):
        tests = {'apple': 2, 'pear': 1, 'computer': 3,
                 'monitor': 3, 'economics': 4, 'echo': 2}
        for k, v in tests.items():
            counted = self.count_syllables_word(k)
            assert counted == v, f'count_syllables_word failed: {k} was counted as {counted}, should be {v}'

    def test_count_syllables_sentence(self):
        tests = {'This is a test sentence.':6,
                    'This is another test sentence':8,
                    'Yet another sentence to be tested.':10}
        for k, v in tests.items():
            counted = self.count_syllables_sentence(k)
            assert counted == v, f'count_syllables_sentence failed: {k} was counted as {counted}, should be {v}'

    def test_count_words_sentence(self):
        tests = {'This is a test sentence.': 5,
                 'This is another test sentence': 5,
                 'Yet another sentence to be tested.': 6}
        for k, v in tests.items():
            counted = self.count_words_sentence(k)
            assert counted == v, f'count_words_sentence failed: {k} was counted as {counted}, should be {v}'


t = TextAnalyzer()
t.test_algos()