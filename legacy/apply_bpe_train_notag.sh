#!/bin/bash 

expdir=$1  # EXPDIR

#`dirname $0`/env.sh
SUBWORD_NMT_DIR="subword-nmt"

data_dir="$expdir/data"
train_file=$data_dir/train
bpe_file=$expdir/bpe/train/train

mkdir -p $expdir/bpe/train

echo "Apply to SRC corpus"

python $SUBWORD_NMT_DIR/subword_nmt/apply_bpe.py \
    -c $expdir/vocab/bpe_codes.32k.SRC_TGT \
    --vocabulary $expdir/vocab/vocab.SRC \
    --vocabulary-threshold 5 \
    --num-workers "-1" \
    < $train_file.SRC \
    > $bpe_file.SRC

echo "Apply to TGT corpus"
    
python $SUBWORD_NMT_DIR/subword_nmt/apply_bpe.py \
    -c $expdir/vocab/bpe_codes.32k.SRC_TGT \
    --vocabulary $expdir/vocab/vocab.TGT \
    --vocabulary-threshold 5 \
    --num-workers "-1" \
    < $train_file.TGT \
    > $bpe_file.TGT

