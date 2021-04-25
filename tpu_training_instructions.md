## Instructions to run on Google cloud TPUs
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
