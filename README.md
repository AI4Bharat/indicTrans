<div align="center">
	<h1><b><i>IndicTrans</i></b></h1>
	<a href="http://indicnlp.ai4bharat.org/samanantar">Website</a> |
	<a href="https://arxiv.org/abs/2104.05596">Paper</a> |
        <a href="https://youtu.be/QwYPOd1eBtQ?t=383">Video</a><br><br>
</div>

**IndicTrans** is a Transformer-4x ( ~434M ) multilingual NMT model trained on [Samanantar](https://indicnlp.ai4bharat.org/samanantar) dataset which is the largest publicly available parallel corpora collection for Indic languages at the time of writing ( 14 April 2021 ). It is a single script model i.e we convert all the Indic data to the Devanagari script which allows for ***better lexical sharing between languages for transfer learning, prevents fragmentation of the subword vocabulary between Indic languages and allows using a smaller subword vocabulary***. We currently release two models - Indic to English and English to Indic and support the following 11 indic languages:

| <!-- -->      | <!-- -->       | <!-- -->     | <!-- -->    |
| ------------- | -------------- | ------------ | ----------- |
| Assamese (as) | Hindi (hi)     | Marathi (mr) | Tamil (ta)  |
| Bengali (bn)  | Kannada (kn)   | Oriya (or)   | Telugu (te) |
| Gujarati (gu) | Malayalam (ml) | Punjabi (pa) |

## Network & Training Details

- Architechture: IndicTrans uses 6 encoder and decoder layers, input embeddings of size 1536 with 16 attention heads and
feedforward dimension of 4096 with total number of parameters of 434M
- Loss: Cross entropy loss
- Optimizer: Adam
- Label Smoothing: 0.1
- Gradient clipping: 1.0
- Learning rate: 5e-4
- Warmup_steps: 4000

Please refer to section 4, 5 of our [paper](https://arxiv.org/ftp/arxiv/papers/2104/2104.05596.pdf) for more details on training/experimental setup.


## Table of contents:
- [Network & Training Details](#network--training-details)
- [Table of contents:](#table-of-contents)
- [Updates](#updates)
- [Download IndicTrans models:](#download-indictrans-models)
- [Trying out the model](#trying-out-the-model)
  - [Huggingface spaces](#huggingface-spaces)
  - [Using our hosted APIs](#using-our-hosted-apis)
  - [Sample screenshot of translate_sentence POST request](#sample-screenshot-of-translate_sentence-post-request)
  - [Command line interface and Python interface for translating text](#command-line-interface-and-python-interface-for-translating-text)
- [Replicate results from our paper:](#replicate-results-from-our-paper)
  - [Setting up your environment](#setting-up-your-environment)
  - [Training the IndicTrans Model](#training-the-indictrans-model)
  - [Getting predictions and computing bleu scores from the trained model](#getting-predictions-and-computing-bleu-scores-from-the-trained-model)
- [Finetuning the model on your input dataset](#finetuning-the-model-on-your-input-dataset)


## Updates
<details><summary>Click to expand </summary>
21 June 2022

```
Add more documentation on hosted API usage
```

18 December 2021

```
Tutorials updated with latest model links
```


26 November 2021
```
 - v0.3 models are now available for download
```

27 June 2021
```
- Updated links for indic to indic model
- Add more comments to training scripts
- Add link to [Samanantar Video](https://youtu.be/QwYPOd1eBtQ?t=383)
- Add folder structure in readme
- Add python wrapper for model inference
```

09 June 2021
```
- Updated links for models
- Added Indic to Indic model
```

09 May 2021
```
- Added fix for finetuning on datasets where some lang pairs are not present. Previously the script assumed the finetuning dataset will have data for all 11 indic lang pairs
- Added colab notebook for finetuning instructions
```
</details>

## Download IndicTrans models:

Indic to English: [v0.3](https://storage.googleapis.com/samanantar-public/V0.3/models/indic-en.zip)

English to Indic: [v0.3](https://storage.googleapis.com/samanantar-public/V0.3/models/en-indic.zip)

Indic to Indic:   [v0.3](https://storage.googleapis.com/samanantar-public/V0.3/models/m2m.zip)

[Mirror links](https://indicnlp.ai4bharat.org/indic-trans/#mirror-links) for the IndicTrans models

## Trying out the model

### Huggingface spaces

- [IndicTrans Indic2English](https://huggingface.co/spaces/ai4bharat/IndicTrans-Indic2English)
- [IndicTrans English2Indic](https://huggingface.co/spaces/ai4bharat/IndicTrans-English2Indic)


### Using our hosted APIs

<details><summary>Click to expand </summary>

Please visit [API documentation](http://216.48.182.174:5050/docs#) to read more about the available API endpoints/methods you can use.

### Sample screenshot of translate_sentence POST request

Go to [API documentation](http://216.48.182.174:5050/docs#), scroll to translate_sentence POST request endpoint and click "Try it out" button.

<br>

<p align="left">
<img src="./sample_images/translate_try_it_out.png" width=50% height=50% />
</p>

<br>

To try english to tamil translation, set the source language to "en" and target language to "ta" and enter your sentence in the "text" field:

<br>

<p align="left">
<img src="./sample_images/translate_en-ta.png" width=50% height=50% />
</p>

<br>

Check the translation result in response:

<p align="left">
<img src="./sample_images/response_en-ta.png" width=50% height=50% />
</p>

<br>

Visit the [API documentation](http://216.48.182.174:5050/docs#)to check other supported methods:

<p align="left">
<img src="./sample_images/api_methods.png" width=50% height=50% />
</p>
</details>

<br>

Refer to this colab notebook on how to use python to hit the API endpoints--> [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/AI4Bharat/indicTrans/blob/main/indicTrans_hosted_api_inference.ipynb)


### Command line interface and Python interface for translating text

The model is trained on single sentences and hence, users need to split parapgraphs to sentences before running the translation when using our command line interface (The python interface has `translate_paragraph` method to handle multi sentence translations).

Note: IndicTrans is trained with a max sequence length of **200** tokens (subwords). If your sentence is too long (> 200 tokens), the sentence will be truncated to 200 tokens before translation.

Here is an example snippet to split paragraphs into sentences for English and Indic languages supported by our model:
```python
# install these libraries
# pip install mosestokenizer
# pip install indic-nlp-library

from mosestokenizer import *
from indicnlp.tokenize import sentence_tokenize

INDIC = ["as", "bn", "gu", "hi", "kn", "ml", "mr", "or", "pa", "ta", "te"]

def split_sentences(paragraph, language):
    if language == "en":
        with MosesSentenceSplitter(language) as splitter:
            return splitter([paragraph])
    elif language in INDIC:
        return sentence_tokenize.sentence_split(paragraph, lang=language)

split_sentences("""COVID-19 is caused by infection with the severe acute respiratory
syndrome coronavirus 2 (SARS-CoV-2) virus strain. The disease is mainly transmitted via the respiratory
route when people inhale droplets and particles that infected people release as they breathe, talk, cough, sneeze, or sing. """, language='en')

>> ['COVID-19 is caused by infection with the severe acute respiratory syndrome coronavirus 2 (SARS-CoV-2) virus strain.',
 'The disease is mainly transmitted via the respiratory route when people inhale droplets and particles that infected people release as they breathe, talk, cough, sneeze, or sing.']

split_sentences("""இத்தொற்றுநோய் உலகளாவிய சமூக மற்றும் பொருளாதார சீர்குலைவை ஏற்படுத்தியுள்ளது.இதனால் பெரும் பொருளாதார மந்தநிலைக்குப் பின்னர் உலகளவில் மிகப்பெரிய மந்தநிலை ஏற்பட்டுள்ளது. இது விளையாட்டு,மத, அரசியல் மற்றும் கலாச்சார நிகழ்வுகளை ஒத்திவைக்க அல்லது ரத்து செய்ய வழிவகுத்தது.
அச்சம் காரணமாக முகக்கவசம், கிருமிநாசினி உள்ளிட்ட பொருட்களை அதிக நபர்கள் வாங்கியதால் விநியோகப் பற்றாக்குறை ஏற்பட்டது.""",
 language='ta')

>> ['இத்தொற்றுநோய் உலகளாவிய சமூக மற்றும் பொருளாதார சீர்குலைவை ஏற்படுத்தியுள்ளது.',
 'இதனால் பெரும் பொருளாதார மந்தநிலைக்குப் பின்னர் உலகளவில் மிகப்பெரிய மந்தநிலை ஏற்பட்டுள்ளது.',
 'இது விளையாட்டு,மத, அரசியல் மற்றும் கலாச்சார நிகழ்வுகளை ஒத்திவைக்க அல்லது ரத்து செய்ய வழிவகுத்தது.',
 'அச்சம் காரணமாக முகக்கவசம், கிருமிநாசினி உள்ளிட்ட பொருட்களை அதிக நபர்கள் வாங்கியதால் விநியோகப் பற்றாக்குறை ஏற்பட்டது.']


```

Follow the colab notebook to setup the environment, download the trained _IndicTrans_ models and translating your own text.

Command line interface --> [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/AI4Bharat/indicTrans/blob/main/indictrans_fairseq_inference.ipynb)


Python interface       --> [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/AI4Bharat/indicTrans/blob/main/indicTrans_python_interface.ipynb)

 The python interface is useful in case you want to reuse the model for multiple translations and do not want to reinitialize the model each time


 ## Replicate results from our paper:
 ###  Setting up your environment
<details><summary>Click to expand </summary>

```bash
cd indicTrans
git clone https://github.com/anoopkunchukuttan/indic_nlp_library.git
git clone https://github.com/anoopkunchukuttan/indic_nlp_resources.git
git clone https://github.com/rsennrich/subword-nmt.git
# install required libraries
pip install sacremoses pandas mock sacrebleu tensorboardX pyarrow indic-nlp-library

# Install fairseq from source
git clone https://github.com/pytorch/fairseq.git
cd fairseq
pip install --editable ./

```
</details>

### Training the IndicTrans Model
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/AI4Bharat/indicTrans/blob/main/IndicTrans_training.ipynb)


Follow the colab notebook to setup the environment, download the Samanantar dataset and train the indicTrans model.

Please refer to this [issue](https://github.com/AI4Bharat/indicTrans/issues/23) to see discussion of our training hyperparameters.

### Getting predictions and computing bleu scores from the trained model

```bash
# To test the models after training, you can use joint_translate.sh



# joint_translate takes src_file, output_fname, src_lang, tgt_lang, model_folder as inputs
# src_file -> input text file to be translated
# output_fname -> name of the output file (will get created) containing the model predictions
# src_lang -> source lang code of the input text ( in this case we are using en-indic model and hence src_lang would be 'en')
# tgt_lang -> target lang code of the input text ( tgt lang for en-indic model would be any of the 11 indic langs we trained on:
#              as, bn, hi, gu, kn, ml, mr, or, pa, ta, te)
# supported languages are:
#              as - assamese, bn - bengali, gu - gujarathi, hi - hindi, kn - kannada,
#              ml - malayalam, mr - marathi, or - oriya, pa - punjabi, ta - tamil, te - telugu

# model_folder -> the directory containing the model and the vocab files



# here we are translating the english sentences to hindi and model_folder contains the model checkpoint
bash joint_translate.sh <path to test.en> en_hi_outputs.txt 'en' 'hi' model_folder

# to compute bleu scores for the predicitions with a reference file, use the following command
# arguments:
# pred_fname: file that contains model predictions
# ref_fname: file that contains references
# src_lang and tgt_lang : the source and target language

bash compute_bleu.sh en_hi_outputs.txt <path to test.hi reference file> 'en' 'hi'

```


 ## Finetuning the model on your input dataset

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/AI4Bharat/indicTrans/blob/main/indicTrans_Finetuning.ipynb)

The colab notebook can be used to setup the environment, download the trained _IndicTrans_ models and prepare your custom dataset for funetuning the indictrans model. There is also a section on mining indic to indic data from english centric corpus for finetuning indic to indic model.

**Note**: Since this is a big model (400M params), you might not be able to train with reasonable batch sizes in the free google Colab account. We are planning to release smaller models (after pruning / distallation) soon.

<!-- ## Mining Indic to Indic pairs from english centric corpus

The `extract_non_english_pairs` in `scripts/extract_non_english_pairs.py` can be used to mine indic to indic pairs from english centric corpus.

As described in the [paper](https://arxiv.org/pdf/2104.05596.pdf) (section 2.5) , we use a very strict deduplication criterion to avoid the creation of very similar parallel sentences. For example, if an en sentence is aligned to *M* hi sentences and *N* ta sentences, then we would get *MN* hi-ta pairs. However, these pairs would be very similar and not contribute much to the training process. Hence, we retain only 1 randomly chosen pair out of these *MN* pairs.

```bash
extract_non_english_pairs(indir, outdir, LANGS):
    """
    Extracts non-english pair parallel corpora
    indir: contains english centric data in the following form:
            - directory named en-xx for language xx
            - each directory contains a train.en and train.xx
    outdir: output directory to store mined data for each pair.
            One directory is created for each pair.
    LANGS: list of languages in the corpus (other than English).
            The language codes must correspond to the ones used in the
            files and directories in indir. Prefarably, sort the languages
            in this list in alphabetic order. outdir will contain data for xx-yy,
            but not for yy-xx, so it will be convenient to have this list in sorted order.
    """
``` -->
