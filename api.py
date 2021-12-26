import time

from fairseq import checkpoint_utils, distributed_utils, options, tasks, utils
from inference.engine import Model
from flask import Flask, request
from flask import jsonify
from flask_cors import CORS, cross_origin
import webvtt
from io import StringIO


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

indic2en_model = Model(expdir='../models/v3/indic-en')
en2indic_model = Model(expdir='../models/v3/en-indic')
m2m_model = Model(expdir='../models/m2m')

language_dict = {
    'Assamese': 'as',
    'Hindi' : 'hi',
    'Marathi' : 'mr',
    'Tamil' : 'ta',
    'Bengali' : 'bn',
    'Kannada' : 'kn',
    'Oriya' : 'or',
    'Telugu' : 'te',
    'Gujarati' : 'gu',
    'Malayalam' : 'ml',
    'Punjabi' : 'pa',
}

def get_inference_params():
    model_type = request.form['model_type']
    source_language = request.form['source_language']
    target_language = request.form['target_language']

    if model_type == 'indic-en':
        model = indic2en_model
        source_lang = language_dict[source_language]
        assert target_language == 'English'
        target_lang = 'en'
    elif model_type == 'en-indic':
        model = en2indic_model
        assert source_language == 'English'
        source_lang = 'en'
        target_lang = language_dict[target_language]
    elif model_type == 'm2m':
        model = m2m_model
        source_lang = language_dict[source_language]
        target_lang = language_dict[target_language]
    
    return model, source_lang, target_lang

@app.route('/', methods=['GET'])
def main():
    return "IndicTrans API"

@app.route("/translate", methods=['POST'])
@cross_origin()
def infer_indic_en():
    model, source_lang, target_lang = get_inference_params()
    source_text = request.form['text']

    start_time = time.time()
    target_text = model.translate_paragraph(source_text, source_lang, target_lang)
    end_time = time.time()
    return {'text':target_text, 'duration':round(end_time-start_time, 2)}

@app.route("/translate_vtt", methods=['POST'])
@cross_origin()
def infer_vtt_indic_en():
    model, source_lang, target_lang = get_inference_params()
    source_text = request.form['text']
    captions = webvtt.read_buffer(StringIO(source_text))
    source_sentences = [caption.text.replace('\r', '').replace('\n', ' ') for caption in captions]

    start_time = time.time()
    target_sentences = model.batch_translate(source_sentences, source_lang, target_lang)
    end_time = time.time()

    for i in range(len(target_sentences)):
        captions[i].text = target_sentences[i]

    return {'text': captions.content, 'duration':round(end_time-start_time, 2)}
