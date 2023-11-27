import streamlit as sl
import tensorflow as tf
from tensorflow.keras.preprocessing.text import tokenizer_from_json
import numpy as np
from streamlit_lottie import st_lottie
import requests as re
import pickle as pe
from language_tool_python import LanguageTool
import json

#tokenizer=Tokenizer()
#load tokenizer
with open('tokenizer_config.json', 'r') as json_file:
    loaded_tokenizer_config = json.load(json_file)

tokenizer = tokenizer_from_json(loaded_tokenizer_config)
#with open('tokenizer_model.pkl', 'rb') as file:
#   tokenizer = pe.load(file)
#tokenizer = pe.load(open('tokenizer_model.pkl','rb'))
#Load Model

model = tf.keras.models.load_model('Chat_pedia_model.h5')


#Function to generate text using the trained model
def generate_text_with_temperature(topic, next_words, temperature=1.0):
    generated_text = topic.lower()
    tool = LanguageTool('en-US')
    for _ in range(next_words):
        token_list = tokenizer.texts_to_sequences([generated_text])[0]
        #seq_length = 30  #Limiting sequence length to 30 words
        token_list = tf.keras.preprocessing.sequence.pad_sequences([token_list], maxlen=30, padding='pre')

        predicted = model.predict(token_list, verbose=0)[-1]  # Last prediction
        predicted = np.log(predicted) / temperature
        exp_preds = np.exp(predicted)
        predicted = exp_preds / np.sum(exp_preds)

        predicted_index = np.random.choice(len(predicted), p=predicted)
        output_word = tokenizer.index_word.get(predicted_index, "")

        generated_text += " " + output_word
        generated_info=tool.correct(generated_text)
    return generated_info

def lottieurl_load(url: str):
    r= re.get(url)
    if r.status_code !=200:
        return None
    return r.json()
lottie_img = lottieurl_load("https://lottie.host/6831e922-4e8c-4f0f-a0e7-d13a8e078042/UtoHLy091O.json")
col1, col2, col3 = sl.columns(3)
with col1:
    sl.write(' ')

with col2:
    st_lottie(lottie_img,speed=1,reverse=False,loop=True,quality="medium",height=200,width=200,key=None)

with col3:
    sl.write(' ')

sl.title("Chat with ChatPedia")

# User input textbox
user_input = sl.text_input("You:", "")

# Button to send user input
if sl.button("Send"):
    # Generate response using the model
    response = generate_text_with_temperature(user_input, next_words=110, temperature=1)
    # Display the model's response
    sl.text_area("Model:", value=response, height=200)