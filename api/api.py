import time

import re
from math import floor, ceil
from fairseq import checkpoint_utils, distributed_utils, options, tasks, utils
# from nltk.tokenize import sent_tokenize
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import webvtt
from io import StringIO
from mosestokenizer import MosesSentenceSplitter

from indicTrans.inference.engine import Model
from punctuate import RestorePuncts
from indicnlp.tokenize.sentence_tokenize import sentence_split

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

indic2en_model = Model(expdir='models/v3/indic-en')
en2indic_model = Model(expdir='models/v3/en-indic')
m2m_model = Model(expdir='models/m2m')

rpunct = RestorePuncts()

indic_language_dict = {
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

splitter = MosesSentenceSplitter('en')

def get_inference_params():
    source_language = request.form['source_language']
    target_language = request.form['target_language']

    if source_language in indic_language_dict and target_language == 'English':
        model = indic2en_model
        source_lang = indic_language_dict[source_language]
        target_lang = 'en'
    elif source_language == 'English' and target_language in indic_language_dict:
        model = en2indic_model
        source_lang = 'en'
        target_lang = indic_language_dict[target_language]
    elif source_language in indic_language_dict and target_language in indic_language_dict:
        model = m2m_model
        source_lang = indic_language_dict[source_language]
        target_lang = indic_language_dict[target_language]
    
    return model, source_lang, target_lang

@app.route('/', methods=['GET'])
def main():
    return "IndicTrans API"

@app.route('/supported_languages', methods=['GET'])
@cross_origin()
def supported_languages():
    return jsonify(indic_language_dict)

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
    start_time = time.time()
    model, source_lang, target_lang = get_inference_params()
    source_text = request.form['text']
    # vad_segments = request.form['vad_nochunk'] # Assuming it is an array of start & end timestamps

    vad = webvtt.read_buffer(StringIO(source_text))
    source_sentences = [v.text.replace('\r', '').replace('\n', ' ') for v in vad]

    ## SUMANTH LOGIC HERE ##

    # for each vad timestamp, do:
    large_sentence = ' '.join(source_sentences) # only sentences in that time range
    large_sentence = large_sentence.lower()
    # split_sents = sentence_split(large_sentence, 'en')
    # print(split_sents)

    large_sentence = re.sub(r'[^\w\s]', '', large_sentence)
    punctuated = rpunct.punctuate(large_sentence, batch_size=32)
    end_time = time.time()
    print("Time Taken for punctuation: {} s".format(end_time - start_time))
    start_time = time.time()
    split_sents = splitter([punctuated]) ### Please uncomment


    # print(split_sents)
    # output_sentence_punctuated = model.translate_paragraph(punctuated, source_lang, target_lang)
    output_sents = model.batch_translate(split_sents, source_lang, target_lang)
    # print(output_sents)
    # output_sents = split_sents
    # print(output_sents)
    # align this to those range of source_sentences in `captions`

    map_ = {split_sents[i] : output_sents[i] for i in range(len(split_sents))}
    # print(map_)
    punct_para = ' '.join(list(map_.keys()))
    nmt_para = ' '.join(list(map_.values()))
    nmt_words = nmt_para.split(' ')

    len_punct = len(punct_para.split(' '))
    len_nmt = len(nmt_para.split(' '))

    start = 0
    for i in range(len(vad)):
        if vad[i].text == '':
            continue

        len_caption = len(vad[i].text.split(' '))
        frac = (len_caption / len_punct)
        # frac = round(frac, 2)

        req_nmt_size = floor(frac * len_nmt)
        # print(frac, req_nmt_size)

        vad[i].text = ' '.join(nmt_words[start:start+req_nmt_size])
        # print(vad[i].text)
        # print(start, req_nmt_size)
        start += req_nmt_size

    end_time = time.time()
    
    print("Time Taken for translation: {} s".format(end_time - start_time))

    # vad.save('aligned.vtt')

    return {
        'text': vad.content,
        # 'duration':round(end_time-start_time, 2)
    }
