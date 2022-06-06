import transformers
from tensorflow import keras

class Model_imdb():
    model = keras.models.load_model('my_model.h5', custom_objects={'TFDistilBertModel': transformers.TFDistilBertModel})
    tokenizer = transformers.AutoTokenizer.from_pretrained('distilbert-base-uncased')

    def get_result(self,text):
        encoded_input = self.tokenizer.encode(text, max_length=400, padding='max_length', truncation=True, return_tensors="tf")
        output = self.model(encoded_input)
        return "Positive" if float(output[0][0]) >= 0.5 else "Negative"