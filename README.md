<div align="center">
	<h1><b><i>IndicTrans</i></b></h1>
	<a href="http://indicnlp.ai4bharat.org">Website</a> | 
	<a href="https://arxiv.org/abs/2104.05596">Paper</a><br><br>
</div>

**IndicTrans** is a Transformer-4x ( 4 times the parameter size of transformer base ) multilingual NMT model trained on [Samanantar](https://indicnlp.ai4bharat.org/samanantar) dataset which is the largest publicly available parallel corpora collection for Indic languages at the time of writing ( 14 April 2021 ). It outperforms commercial translation systems and existing models on a wide variety of benchmarks (See the result section for more details)

It is a single script model i.e we convert all the Indic data to the Devanagari script which allows for ***better lexical sharing between languages for transfer learning, prevents fragmentation of the subword vocabulary between Indic languages and allows using a smaller subword vocabulary***. We currently release two models - Indic to English and English to Indic and support these 11 indic languages: 

| <!-- -->  | <!-- --> | <!-- --> | <!-- --> |
| ------------- | ------------- | ------------- | ------------- |
| Assamese (as)  | Hindi (hi) | Marathi (mr) | Tamil (ta)|
| Bengali (bn) | Kannada (kn)| Oriya (or) | Telugu (te)|
| Gujarati (gu) | Malayalam (ml) | Punjabi (pa) |


## Using the model for inference
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/gowtham1997/indicTrans/blob/main/indictrans_fairseq_inference.ipynb)

^ follow the instructions here to setup the environment with required libraries, download the pretrained models and run inference


## Needed

 Clone these repositories and keep them under the mentioned folder_names:

indic_nlp_library    - clone this [repo](https://github.com/anoopkunchukuttan/indic_nlp_library)

indic_nlp_resources  - clone this [repo](https://github.com/anoopkunchukuttan/indic_nlp_resources)

subword-nmt          - clone this [repo](https://github.com/rsennrich/subword-nmt.git)

(or)

```bash
git clone https://github.com/anoopkunchukuttan/indic_nlp_library.git
git clone https://github.com/anoopkunchukuttan/indic_nlp_resources.git
git clone https://github.com/rsennrich/subword-nmt.git
```


## Model

- transformer base
- 32k vocab (src as well as target)
- BPE (subword-nmt)
- 95m params

## How to train the indictrans model on custom training data?

We will update this section soon.

## Instructions to run on Google cloud TPUs
<details><summary>Click to expand </summary>
Before starting these steps, make sure to prepare the dataset (normalization -> bpe -> .. -> binarization) following the steps in indicTrans workflow or do these steps on a cpu instance before launching the tpu instance (to save time and costs)

### Creating TPU instance

- Create a cpu instance on gcp with `torch-xla` image like:
```bash
gcloud compute --project=${PROJECT_ID} instances create <name for your instance> \
  --zone=<zone>  \
  --machine-type=n1-standard-16  \
  --image-family=torch-xla \
  --image-project=ml-images  \
  --boot-disk-size=200GB \
  --scopes=https://www.googleapis.com/auth/cloud-platform
```
- Once the instance is created, Launch a Cloud TPU (from your cpu vm instance) using the following command (you can change the `accelerator_type` according to your needs):
```bash
gcloud compute tpus create <name for your TPU> \
--zone=<zone> \
--network=default \
--version=pytorch-1.7 \
--accelerator-type=v3-8
```
                                          (or)
Create a new tpu using the GUI in https://console.cloud.google.com/compute/tpus and make sure to select `version` as  `pytorch 1.7`.

- Once the tpu is launched, identify its ip address:
```bash
# you can run this inside cpu instance and note down the IP address which is located under the NETWORK_ENDPOINTS column
gcloud compute tpus list --zone=us-central1-a
```
                                          (or)
Go to https://console.cloud.google.com/compute/tpus and note down ip address for the created TPU from the `interal ip` column

### Installing Fairseq, getting data on the cpu instance

- Activate the `torch xla 1.7` conda environment and install necessary libs for IndicTrans (**Excluding FairSeq**):
```bash
conda activate torch-xla-1.7
pip install sacremoses pandas mock sacrebleu tensorboardX pyarrow
```
- Configure environment variables for TPU:
```bash
export TPU_IP_ADDRESS=ip-address; \
export XRT_TPU_CONFIG="tpu_worker;0;$TPU_IP_ADDRESS:8470"
```
- Download the prepared binarized data for FairSeq

- Clone the latest version of Fairseq (this supports tpu) and install from source. There is an [issue](https://github.com/pytorch/fairseq/issues/3259) with the latest commit and hence we use a different commit to install from source (This may have been fixed in the latest master but we have not tested it.)
```bash
git clone https://github.com/pytorch/fairseq.git
git checkout da9eaba12d82b9bfc1442f0e2c6fc1b895f4d35d
pip install --editable ./
```

- Start TPU training
```bash
# this is for using all tpu cores
export MKL_SERVICE_FORCE_INTEL=1

fairseq-train   {expdir}/exp2_m2o_baseline/final_bin \
--max-source-positions=200 \
--max-target-positions=200 \
--max-update=1000000 \
--save-interval=5   \
--arch=transformer  \
--attention-dropout=0.1   \
--criterion=label_smoothed_cross_entropy   \
--source-lang=SRC   \
--lr-scheduler=inverse_sqrt   \
--skip-invalid-size-inputs-valid-test   \
--target-lang=TGT   \
--label-smoothing=0.1   \
--update-freq=1   \
--optimizer adam   \
--adam-betas '(0.9, 0.98)'   \
--warmup-init-lr 1e-07   \
--lr 0.0005   \
--warmup-updates 4000   \
--dropout 0.2 \
--weight-decay 0.0  \
--tpu \
--distributed-world-size 8   \
--max-tokens 8192 \
--num-batch-buckets 8 \
--tensorboard-logdir  {expdir}/exp2_m2o_baseline/tensorboard  \
--save-dir {expdir}/exp2_m2o_baseline/model \
--keep-last-epochs 5 \
--patience 5
```

**Note** While training, we noticed that the training was slower on tpus, compared to using multiple GPUs, we have documented some issues and [filed an issue](https://github.com/pytorch/fairseq/issues/3317) at fairseq repo for advice. We'll update this section as we learn more about efficient training on TPUs. Also feel free to open an issue/pull request if you find a bug or know an efficient method to make code train faster on tpus.

</details>

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
- Anoop Kunchukuttan, <sub>([Microsoft](https://www.microsoft.com/en-in/), [AI4Bharat](https://ai4bharat.org))</sub>
- Pratyush Kumar, <sub>([RBCDSAI](https://rbcdsai.iitm.ac.in), [AI4Bharat](https://ai4bharat.org), [IITM](https://www.iitm.ac.in))</sub>
- Mitesh Shantadevi Khapra, <sub>([RBCDSAI](https://rbcdsai.iitm.ac.in), [AI4Bharat](https://ai4bharat.org), [IITM](https://www.iitm.ac.in))</sub>



### Contact

- Anoop Kunchukuttan ([anoop.kunchukuttan@gmail.com](mailto:anoop.kunchukuttan@gmail.com))
- Mitesh Khapra ([miteshk@cse.iitm.ac.in](mailto:miteshk@cse.iitm.ac.in))
- Pratyush Kumar ([pratyush@cse.iitm.ac.in](mailto:pratyush@cse.iitm.ac.in))
