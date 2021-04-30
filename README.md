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

## Download IndicTrans models:

Indic to English: [V0.2](https://akpublicdata.blob.core.windows.net/indicnlp/indictrans/indictrans-indic-en-v0.2.zip)

English to Indic: [V0.2](https://akpublicdata.blob.core.windows.net/indicnlp/indictrans/inidctrans-en-indic-v0.2.zip)


## Using the model for translating any input

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/AI4Bharat/indicTrans/blob/main/indictrans_fairseq_inference.ipynb)

The colab notebook can be used to setup the environment, download the trained _IndicTrans_ models and translating your own text.


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
