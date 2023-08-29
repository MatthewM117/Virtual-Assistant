import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
import tensorflow as tf

lemmatizer = WordNetLemmatizer()

model = None

# ensure the model is only loaded once
def load_virtual_assistant_model():
    global model
    if model is None:
        #interpreter = tf.lite.Interpreter(model_path='/home/matthewm1/mysite/tf_lite_model.tflite')
        interpreter = tf.lite.Interpreter(model_path='virtual_assistant_model.tflite')
        print("HERE")
        interpreter.allocate_tensors()
        model = interpreter

load_virtual_assistant_model()

def get_intents():
    #return json.loads(open('/home/matthewm1/mysite/intents.json').read())
    return json.loads(open('intents.json').read())

#words = pickle.load(open('/home/matthewm1/mysite/words.pkl', 'rb')) # rb = read binary
#classes = pickle.load(open('/home/matthewm1/mysite/classes.pkl', 'rb'))
words = pickle.load(open('words.pkl', 'rb')) # rb = read binary
classes = pickle.load(open('classes.pkl', 'rb'))

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1

    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    input_details = model.get_input_details()
    output_details = model.get_output_details()

    bow = np.array([bow], dtype=np.float32)
    model.set_tensor(input_details[0]['index'], bow)
    model.invoke()

    output_data = model.get_tensor(output_details[0]['index'])
    ERROR_THRESHOLD = 0.25 # 25%
    results = [(i, r) for i, r in enumerate(output_data[0]) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)

    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})

    return return_list

def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break

    return result

if __name__ == '__main__':
    intents = get_intents()
    ints = predict_class("i pooted")
    print(ints[0]['probability'])
    ai_response = get_response(ints, intents)
    print(ai_response)