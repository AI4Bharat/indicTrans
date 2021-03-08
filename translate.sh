#!/bin/bash
echo `date`
infname=$1
outfname=$2
src_lang=$3
tgt_lang=$4
exp_dir=$5
ref_fname=$6

#`dirname $0`/env.sh
SUBWORD_NMT_DIR='subword-nmt'
model_dir=$exp_dir/model
data_bin_dir=$exp_dir/final_bin

### normalization and script conversion 

echo "Applying normalization and script conversion"
input_size=`python preprocess_translate.py $infname $outfname.norm $src_lang`
echo "Number of sentences in input: $input_size"

### apply BPE to input file 

echo "Applying BPE"
python $SUBWORD_NMT_DIR/subword_nmt/apply_bpe.py \
    -c $exp_dir/vocab/bpe_codes.32k.SRC_TGT \
    --vocabulary $exp_dir/vocab/vocab.SRC \
    --vocabulary-threshold 5 \
    < $outfname.norm \
    > $outfname._bpe

echo "Adding language tags"
python add_tags_translate.py $outfname._bpe $outfname.bpe $src_lang $tgt_lang

### run decoder 

echo "Decoding"
    
src_input_bpe_fname=$outfname.bpe
tgt_output_fname=$outfname
fairseq-interactive  $data_bin_dir \
    -s SRC -t TGT\
    --tpu --distributed-world-size 1  \
    --path $model_dir/checkpoint_best.pt \
    --batch-size 512  --buffer-size 5000 --beam 5  --remove-bpe \
    --skip-invalid-size-inputs-valid-test \
    --input $src_input_bpe_fname  >  $tgt_output_fname.log 2>&1


echo "Extracting translations, script conversion and detokenization"
python postprocess_translate.py $tgt_output_fname.log $tgt_output_fname $input_size $tgt_lang
sacrebleu $ref_fname < $tgt_output_fname
echo `date`
echo "Translation completed"
