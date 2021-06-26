<div align="center">
	<h1><b><i>IndicTrans</i></b></h1>
	<a href="http://indicnlp.ai4bharat.org/samanantar">Website</a> |
	<a href="https://arxiv.org/abs/2104.05596">Paper</a><br><br>
</div>

**IndicTrans** is a Transformer-4x ( ~434M ) multilingual NMT model trained on [Samanantar](https://indicnlp.ai4bharat.org/samanantar) dataset which is the largest publicly available parallel corpora collection for Indic languages at the time of writing ( 14 April 2021 ). It is a single script model i.e we convert all the Indic data to the Devanagari script which allows for ***better lexical sharing between languages for transfer learning, prevents fragmentation of the subword vocabulary between Indic languages and allows using a smaller subword vocabulary***. We currently release two models - Indic to English and English to Indic and support the following 11 indic languages:

| <!-- -->  | <!-- --> | <!-- --> | <!-- --> |
| ------------- | ------------- | ------------- | ------------- |
| Assamese (as)  | Hindi (hi) | Marathi (mr) | Tamil (ta)|
| Bengali (bn) | Kannada (kn)| Oriya (or) | Telugu (te)|
| Gujarati (gu) | Malayalam (ml) | Punjabi (pa) |


## Updates

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


## Download IndicTrans models:

Indic to English: [V0.2](https://storage.googleapis.com/samanantar-public/V0.2/models/indic-en.zip)

English to Indic: [V0.2](https://storage.googleapis.com/samanantar-public/V0.2/models/en-indic.zip)

Indic to Indic:   [V0.3](https://storage.googleapis.com/samanantar-public/V0.3/models/m2m.zip)


## Using the model for translating any input

The model is trained on single sentences and hence, users need to split parapgraphs to sentences before running the translation. Here is an example snippet to split paragraphs into sentences for English and Indic languages supported by our model:
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

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/AI4Bharat/indicTrans/blob/main/indictrans_fairseq_inference.ipynb)


## Finetuning the model on your input dataset

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/AI4Bharat/indicTrans/blob/main/indicTrans_Finetuning.ipynb)

The colab notebook can be used to setup the environment, download the trained _IndicTrans_ models and prepare your custom dataset for funetuning the indictrans model. There is also a section on mining indic to indic data from english centric corpus for finetuning indic to indic model.

**Note**: Since this is a big model (400M params), you might not be able to train with reasonable batch sizes in the free google Colab account. We are planning to release smaller models (after pruning / distallation) soon.

## Mining Indic to Indic pairs from english centric corpus

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
```

## Installation
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

## How to train the indictrans model on custom training data?

Will be updated soon.


## Citing

If you are using any of the resources, please cite the following article:
```
@misc{ramesh2021samanantar,
      title={Samanantar: The Largest Publicly Available Parallel Corpora Collection for 11 Indic Languages},
      author={Gowtham Ramesh and Sumanth Doddapaneni and Aravinth Bheemaraj and Mayank Jobanputra and Raghavan AK and Ajitesh Sharma and Sujit Sahoo and Harshita Diddee and Mahalakshmi J and Divyanshu Kakwani and Navneet Kumar and Aswin Pradeep and Kumar Deepak and Vivek Raghavan and Anoop Kunchukuttan and Pratyush Kumar and Mitesh Shantadevi Khapra},
      year={2021},
      eprint={2104.05596},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```

We would like to hear from you if:

- You are using our resources. Please let us know how you are putting these resources to use.
- You have any feedback on these resources.



### License

The IndicTrans code (and models) are released under the MIT License.


### Contributors

- Gowtham Ramesh, <sub>([RBCDSAI](https://rbcdsai.iitm.ac.in), [IITM](https://www.iitm.ac.in))</sub>
- Sumanth Doddapaneni, <sub>([RBCDSAI](https://rbcdsai.iitm.ac.in), [IITM](https://www.iitm.ac.in))</sub>
- Aravinth Bheemaraj, <sub>([Tarento](https://www.linkedin.com/company/tarento-group/), [EkStep](https://ekstep.in))</sub>
- Mayank Jobanputra, <sub>([IITM](https://www.iitm.ac.in))</sub>
- Raghavan AK, <sub>([AI4Bharat](https://ai4bharat.org))</sub>
- Ajitesh Sharma, <sub>([Tarento](https://www.linkedin.com/company/tarento-group/), [EkStep](https://ekstep.in))</sub>
- Sujit Sahoo, <sub>([Tarento](https://www.linkedin.com/company/tarento-group/), [EkStep](https://ekstep.in))</sub>
- Harshita Diddee, <sub>([AI4Bharat](https://ai4bharat.org))</sub>
- Mahalakshmi J, <sub>([AI4Bharat](https://ai4bharat.org))</sub>
- Divyanshu Kakwani, <sub>([IITM](https://www.iitm.ac.in), [AI4Bharat](https://ai4bharat.org))</sub>
- Navneet Kumar, <sub>([Tarento](https://www.linkedin.com/company/tarento-group/), [EkStep](https://ekstep.in))</sub>
- Aswin Pradeep, <sub>([Tarento](https://www.linkedin.com/company/tarento-group/), [EkStep](https://ekstep.in))</sub>
- Kumar Deepak, <sub>([Tarento](https://www.linkedin.com/company/tarento-group/), [EkStep](https://ekstep.in))</sub>
- Vivek Raghavan, <sub>([EkStep](https://ekstep.in))</sub>
- Anoop Kunchukuttan, <sub>([Microsoft](https://www.microsoft.com/en-in/), [AI4Bharat](https://ai4bharat.org))</sub>
- Pratyush Kumar, <sub>([RBCDSAI](https://rbcdsai.iitm.ac.in), [AI4Bharat](https://ai4bharat.org), [IITM](https://www.iitm.ac.in))</sub>
- Mitesh Shantadevi Khapra, <sub>([RBCDSAI](https://rbcdsai.iitm.ac.in), [AI4Bharat](https://ai4bharat.org), [IITM](https://www.iitm.ac.in))</sub>



### Contact

- Anoop Kunchukuttan ([anoop.kunchukuttan@gmail.com](mailto:anoop.kunchukuttan@gmail.com))
- Mitesh Khapra ([miteshk@cse.iitm.ac.in](mailto:miteshk@cse.iitm.ac.in))
- Pratyush Kumar ([pratyush@cse.iitm.ac.in](mailto:pratyush@cse.iitm.ac.in))
