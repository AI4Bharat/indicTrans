#!/bin/bash
echo `date`
srcfname=$1
tgtfname=$2
outfname=$3
src_lang=$4
tgt_lang=$5
exp_dir=$6
ref_fname=$7

SRC_PREFIX='SRC'
TGT_PREFIX='TGT'

#`dirname $0`/env.sh
SUBWORD_NMT_DIR='subword-nmt'
model_dir=$exp_dir/model
data_bin_dir=$exp_dir/final_bin

### normalization and script conversion

echo "Applying normalization and script conversion"
input_size=`python scripts/preprocess_translate.py $srcfname $outfname.$src_lang.norm $src_lang true`
input_size=`python scripts/preprocess_translate.py $tgtfname $outfname.$tgt_lang.norm $tgt_lang true`
echo "Number of sentences in input: $input_size"

### apply BPE to input file

echo "Applying BPE to src input"
python $SUBWORD_NMT_DIR/subword_nmt/apply_bpe.py \
    -c $exp_dir/vocab/bpe_codes.32k.${SRC_PREFIX} \
    --vocabulary $exp_dir/vocab/vocab.$SRC_PREFIX \
    --vocabulary-threshold 5 \
    < $outfname.$src_lang.norm \
    > $outfname.$src_lang._bpe

# not needed for joint training
# echo "Adding language tags"
python scripts/add_tags_translate.py $outfname.$src_lang._bpe $outfname.$src_lang.bpe $src_lang $tgt_lang

echo "Applying BPE to tgt input"
python $SUBWORD_NMT_DIR/subword_nmt/apply_bpe.py \
    -c $exp_dir/vocab/bpe_codes.32k.${TGT_PREFIX} \
    --vocabulary $exp_dir/vocab/vocab.$TGT_PREFIX \
    --vocabulary-threshold 5 \
    < $outfname.$tgt_lang.norm \
    > $outfname.$tgt_lang.bpe


### pre-process to binarize data 

cp  $outfname.$src_lang.bpe $outfname.$SRC_PREFIX
cp  $outfname.$tgt_lang.bpe $outfname.$TGT_PREFIX
inputproc_data_dir=$outfname.data_bin

num_workers=`python -c "import multiprocessing; print(multiprocessing.cpu_count())"`

rm -rf $inputproc_data_dir
mkdir -p $inputproc_data_dir
fairseq-preprocess --source-lang $SRC_PREFIX --target-lang $TGT_PREFIX \
 --testpref $outfname \
 --destdir $inputproc_data_dir --workers $num_workers \
 --srcdict $data_bin_dir/dict.SRC.txt --tgtdict $data_bin_dir/dict.TGT.txt --thresholdtgt 5 --thresholdsrc 5  

### run scorer 

echo "Scoring"

src_input_bpe_fname=$outfname.$SRC_PREFIX
src_output_bpe_fname=$outfname.$TGT_PREFIX
tgt_output_fname=$outfname
fairseq-generate  $inputproc_data_dir \
    -s $SRC_PREFIX -t $TGT_PREFIX \
    --distributed-world-size 1  \
    --path $model_dir/checkpoint_best.pt \
    --gen-subset test \
    --batch-size 256  --remove-bpe \
    --skip-invalid-size-inputs-valid-test \
    --user-dir model_configs \
    --score-reference >  $tgt_output_fname.log 2>&1

echo "Extracting translations, script conversion and detokenization"
# this part reverses the transliteration from devnagiri script to target lang and then detokenizes it.
python scripts/postprocess_score.py $tgt_output_fname.log $tgt_output_fname $input_size 

echo "Scoring completed. Generated output file: $outfname"
