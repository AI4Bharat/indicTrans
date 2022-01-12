# -*- coding: utf-8 -*-
# 💾⚙️🔮

# taken from https://github.com/Felflare/rpunct/blob/master/rpunct/punctuate.py
# modified to support batching during gpu inference


__author__ = "Daulet N."
__email__ = "daulet.nurmanbetov@gmail.com"

import time
import logging
import webvtt
import torch
from io import StringIO
from nltk.tokenize import sent_tokenize
#from langdetect import detect
from simpletransformers.ner import NERModel


class RestorePuncts:
    def __init__(self, wrds_per_pred=250):
        self.wrds_per_pred = wrds_per_pred
        self.overlap_wrds = 30
        self.valid_labels = ['OU', 'OO', '.O', '!O', ',O', '.U', '!U', ',U', ':O', ';O', ':U', "'O", '-O', '?O', '?U']
        self.model = NERModel("bert", "felflare/bert-restore-punctuation", labels=self.valid_labels,
                              args={"silent": True, "max_seq_length": 512})
        # use_cuda isnt working and this hack seems to load the model correctly to the gpu
        self.model.device = torch.device("cuda:1")
        # dummy punctuate to load the model onto gpu
        self.punctuate("hello how are you")

    def punctuate(self, text: str, batch_size:int=32, lang:str=''):
        """
        Performs punctuation restoration on arbitrarily large text.
        Detects if input is not English, if non-English was detected terminates predictions.
        Overrride by supplying `lang='en'`
        
        Args:
            - text (str): Text to punctuate, can be few words to as large as you want.
            - lang (str): Explicit language of input text.
        """
        #if not lang and len(text) > 10:
        #    lang = detect(text)
        #if lang != 'en':
        #    raise Exception(F"""Non English text detected. Restore Punctuation works only for English.
        #    If you are certain the input is English, pass argument lang='en' to this function.
        #    Punctuate received: {text}""")

        def chunks(L, n):
            return [L[x : x + n] for x in range(0, len(L), n)]



        # plit up large text into bert digestable chunks
        splits = self.split_on_toks(text, self.wrds_per_pred, self.overlap_wrds)

        texts = [i["text"] for i in splits]
        batches = chunks(texts, batch_size)
        preds_lst = []


        for batch in batches:
            batch_preds, _ = self.model.predict(batch)
            preds_lst.extend(batch_preds)

        
        # predict slices
        # full_preds_lst contains tuple of labels and logits
        #full_preds_lst = [self.predict(i['text']) for i in splits]
        # extract predictions, and discard logits
        #preds_lst = [i[0][0] for i in full_preds_lst]
        # join text slices
        combined_preds = self.combine_results(text, preds_lst)
        # create punctuated prediction
        punct_text = self.punctuate_texts(combined_preds)
        return punct_text

    def predict(self, input_slice):
        """
        Passes the unpunctuated text to the model for punctuation.
        """
        predictions, raw_outputs = self.model.predict([input_slice])
        return predictions, raw_outputs

    @staticmethod
    def split_on_toks(text, length, overlap):
        """
        Splits text into predefined slices of overlapping text with indexes (offsets)
        that tie-back to original text.
        This is done to bypass 512 token limit on transformer models by sequentially
        feeding chunks of < 512 toks.
        Example output:
        [{...}, {"text": "...", 'start_idx': 31354, 'end_idx': 32648}, {...}]
        """
        wrds = text.replace('\n', ' ').split(" ")
        resp = []
        lst_chunk_idx = 0
        i = 0

        while True:
            # words in the chunk and the overlapping portion
            wrds_len = wrds[(length * i):(length * (i + 1))]
            wrds_ovlp = wrds[(length * (i + 1)):((length * (i + 1)) + overlap)]
            wrds_split = wrds_len + wrds_ovlp

            # Break loop if no more words
            if not wrds_split:
                break

            wrds_str = " ".join(wrds_split)
            nxt_chunk_start_idx = len(" ".join(wrds_len))
            lst_char_idx = len(" ".join(wrds_split))

            resp_obj = {
                "text": wrds_str,
                "start_idx": lst_chunk_idx,
                "end_idx": lst_char_idx + lst_chunk_idx,
            }

            resp.append(resp_obj)
            lst_chunk_idx += nxt_chunk_start_idx + 1
            i += 1
        logging.info(f"Sliced transcript into {len(resp)} slices.")
        return resp

    @staticmethod
    def combine_results(full_text: str, text_slices):
        """
        Given a full text and predictions of each slice combines predictions into a single text again.
        Performs validataion wether text was combined correctly
        """
        split_full_text = full_text.replace('\n', ' ').split(" ")
        split_full_text = [i for i in split_full_text if i]
        split_full_text_len = len(split_full_text)
        output_text = []
        index = 0

        if len(text_slices[-1]) <= 3 and len(text_slices) > 1:
            text_slices = text_slices[:-1]

        for _slice in text_slices:
            slice_wrds = len(_slice)
            for ix, wrd in enumerate(_slice):
                # print(index, "|", str(list(wrd.keys())[0]), "|", split_full_text[index])
                if index == split_full_text_len:
                    break

                if split_full_text[index] == str(list(wrd.keys())[0]) and \
                        ix <= slice_wrds - 3 and text_slices[-1] != _slice:
                    index += 1
                    pred_item_tuple = list(wrd.items())[0]
                    output_text.append(pred_item_tuple)
                elif split_full_text[index] == str(list(wrd.keys())[0]) and text_slices[-1] == _slice:
                    index += 1
                    pred_item_tuple = list(wrd.items())[0]
                    output_text.append(pred_item_tuple)
        assert [i[0] for i in output_text] == split_full_text
        return output_text

    @staticmethod
    def punctuate_texts(full_pred: list):
        """
        Given a list of Predictions from the model, applies the predictions to text,
        thus punctuating it.
        """
        punct_resp = ""
        for i in full_pred:
            word, label = i
            if label[-1] == "U":
                punct_wrd = word.capitalize()
            else:
                punct_wrd = word

            if label[0] != "O":
                punct_wrd += label[0]

            punct_resp += punct_wrd + " "
        punct_resp = punct_resp.strip()
        # Append trailing period if doesnt exist.
        if punct_resp[-1].isalnum():
            punct_resp += "."
        return punct_resp


if __name__ == "__main__":

    start = time.time()
    punct_model = RestorePuncts()

    load_model = time.time()
    print(f'Time to load model: {load_model - start}')
    # read test file
    # with open('en_lower.txt', 'r') as fp:
    #     # test_sample = fp.read()
    #     lines = fp.readlines()

    with open('sample.vtt', 'r') as fp:
        source_text = fp.read()

    # captions = webvtt.read_buffer(StringIO(source_text))
    captions = webvtt.read('sample.vtt')
    source_sentences = [caption.text.replace('\r', '').replace('\n', ' ') for caption in captions]

    # print(source_sentences)

    sent = ' '.join(source_sentences)
    punctuated = punct_model.punctuate(sent)

    tokenised = sent_tokenize(punctuated)
    # print(tokenised)

    for i in range(len(tokenised)):
        captions[i].text = tokenised[i]
    # return captions.content
    captions.save('my_captions.vtt')

    end = time.time()
    print(f'Time for run: {end - load_model}')
    print(f'Total time: {end  - start}')
