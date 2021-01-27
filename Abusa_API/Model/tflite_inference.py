import tflite_runtime.interpreter as tflite
import numpy as np
import re
from nltk.corpus import stopwords
import pickle

### todo replace the dependency
# from keras.preprocessing.sequence import pad_sequences
###

class Processor:
    def __init__(self, model_path="model.tflite", tokenizer_path="tokenizer.pickle", MAX_SEQUENCE_LENGTH=400, thresh=0.6):
        self.labels = ['Hate', 'Insult', 'Obscene', 'Severe Toxic', 'Threat', 'Toxic']
        self.MAX_SEQUENCE_LENGTH = MAX_SEQUENCE_LENGTH
        self.thresh = thresh
        self.model_path = model_path
        self.tokenizer_path = tokenizer_path
        self.load_model()

    def load_model(self):
        self.interpreter = tflite.Interpreter(model_path=self.model_path)
        self.interpreter.allocate_tensors()

        # Get input and output tensors.
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        self.input_shape = self.input_details[0]['shape']

        with open(self.tokenizer_path, 'rb') as f:
            self.tokenizer = pickle.load(f)

    def decontracted(self, phrase):
        # specific
        phrase = re.sub(r"won't", "will not", phrase)
        phrase = re.sub(r"can\'t", "can not", phrase)
        # general
        phrase = re.sub(r"n\'t", " not", phrase)
        phrase = re.sub(r"\'re", " are", phrase)
        phrase = re.sub(r"\'s", " is", phrase)
        phrase = re.sub(r"\'d", " would", phrase)
        phrase = re.sub(r"\'ll", " will", phrase)
        phrase = re.sub(r"\'t", " not", phrase)
        phrase = re.sub(r"\'ve", " have", phrase)
        phrase = re.sub(r"\'m", " am", phrase)
        return phrase
    
    # def pad_sequences(self, data, maxlen):
    #     r = len(data)
    #     c = np.max(np.array(data, dtype=np.object))
    #     c = 1 if isinstance(c, (int,float)) else len(c)
    #     c = c if c == maxlen else maxlen

    #     l = []
    #     for i in data:
    #         required_elements = c - len(i)
    #         l.append([0 for x in range(required_elements)]+i[:c])

    #     return np.array(l, dtype=np.float32)
    def pad_sequences(self, sequences, maxlen=None, dtype='int32', padding='pre', truncating='pre', value=0.):
        """Pads sequences to the same length.
        This function transforms a list of
        `num_samples` sequences (lists of integers)
        into a 2D Numpy array of shape `(num_samples, num_timesteps)`.
        `num_timesteps` is either the `maxlen` argument if provided,
        or the length of the longest sequence otherwise.
        Sequences that are shorter than `num_timesteps`
        are padded with `value` at the beginning or the end
        if padding='post.
        Sequences longer than `num_timesteps` are truncated
        so that they fit the desired length.
        The position where padding or truncation happens is determined by
        the arguments `padding` and `truncating`, respectively.
        Pre-padding is the default.
        # Arguments
            sequences: List of lists, where each element is a sequence.
            maxlen: Int, maximum length of all sequences.
            dtype: Type of the output sequences.
                To pad sequences with variable length strings, you can use `object`.
            padding: String, 'pre' or 'post':
                pad either before or after each sequence.
            truncating: String, 'pre' or 'post':
                remove values from sequences larger than
                `maxlen`, either at the beginning or at the end of the sequences.
            value: Float or String, padding value.
        # Returns
            x: Numpy array with shape `(len(sequences), maxlen)`
        # Raises
            ValueError: In case of invalid values for `truncating` or `padding`,
                or in case of invalid shape for a `sequences` entry.
        """
        if not hasattr(sequences, '__len__'):
            raise ValueError('`sequences` must be iterable.')
        num_samples = len(sequences)

        lengths = []
        sample_shape = ()
        flag = True

        # take the sample shape from the first non empty sequence
        # checking for consistency in the main loop below.

        for x in sequences:
            try:
                lengths.append(len(x))
                if flag and len(x):
                    sample_shape = np.asarray(x).shape[1:]
                    flag = False
            except TypeError:
                raise ValueError('`sequences` must be a list of iterables. '
                                'Found non-iterable: ' + str(x))

        if maxlen is None:
            maxlen = np.max(lengths)

        is_dtype_str = np.issubdtype(dtype, np.str_) or np.issubdtype(dtype, np.unicode_)
        if isinstance(value, str) and dtype != object and not is_dtype_str:
            raise ValueError("`dtype` {} is not compatible with `value`'s type: {}\n"
                            "You should set `dtype=object` for variable length strings."
                            .format(dtype, type(value)))

        x = np.full((num_samples, maxlen) + sample_shape, value, dtype=dtype)
        for idx, s in enumerate(sequences):
            if not len(s):
                continue  # empty list/array was found
            if truncating == 'pre':
                trunc = s[-maxlen:]
            elif truncating == 'post':
                trunc = s[:maxlen]
            else:
                raise ValueError('Truncating type "%s" '
                                'not understood' % truncating)

            # check `trunc` has expected shape
            trunc = np.asarray(trunc, dtype=dtype)
            if trunc.shape[1:] != sample_shape:
                raise ValueError('Shape of sample %s of sequence at position %s '
                                'is different from expected shape %s' %
                                (trunc.shape[1:], idx, sample_shape))

            if padding == 'post':
                x[idx, :len(trunc)] = trunc
            elif padding == 'pre':
                x[idx, -len(trunc):] = trunc
            else:
                raise ValueError('Padding type "%s" not understood' % padding)
        return x
        
    def tokenize(self, data):
        test_sequences = self.tokenizer.texts_to_sequences([data])
        test_data = self.pad_sequences(test_sequences, maxlen=self.MAX_SEQUENCE_LENGTH)
        return test_data.astype('float32') 

    def clean_punctuation(self, sentence):
        cleaned = re.sub(r'[?|!|\'|"|#]',r'',sentence)
        cleaned = re.sub(r'[.|,|)|(|\|/]',r' ',cleaned)
        cleaned = cleaned.strip()
        cleaned = cleaned.replace("\n"," ")
        return cleaned

    def clear_sentence(self, sentence):
        sentence = re.sub(r"http\S+", "", sentence)
        sentence = self.decontracted(sentence)
        sentence = self.clean_punctuation(sentence)
        sentence = re.sub("\S*\d\S*", "", sentence).strip()
        sentence = re.sub('[^A-Za-z]+', ' ', sentence)
        stop_words = set(stopwords.words('english'))

        stop_words.update(['zero','one','two','three','four','five','six','seven','eight','nine','ten','may','also','across','among','beside','however','yet','within'])
        sentence = ' '.join(e.lower() for e in sentence.split() if e.lower() not in  stopwords.words('english'))
        return sentence.strip()

    def preprocess(self, data):
        [d.update({'raw': self.tokenize(self.clear_sentence(' '.join(d.get('data'))))}) for d in data]
        return data

    def get_prediction(self, data):
        data = self.preprocess(data)

        new_data = []

        for d in data:
            raw = d.pop('raw')
            self.interpreter.set_tensor(self.input_details[0]['index'], raw)
            self.interpreter.invoke()
            output_data = self.interpreter.get_tensor(self.output_details[0]['index'])
            predictions = dict(zip(self.labels, output_data[0].tolist()))
            d.update({'predictions': predictions, 'p': 1 if max(predictions.values()) > self.thresh else 0})
            
            if d['p'] == 1:
                new_data.append(d)

        return new_data

if __name__ == "__main__":
    data = [{'id': '0', 'data': ['Fuck', 'this', 'world']}, {'id': '1', 'data': ['He', 'is', 'cute']}]

    p = Processor()
    r = p.get_prediction(data)

    print(r)