#!/bin/bash 

expdir=$1  # EXPDIR

#`dirname $0`/env.sh
SUBWORD_NMT_DIR="subword-nmt"
data_dir="$expdir/data"
train_file=$data_dir/train
num_operations=32000

echo Input file: $train_file

mkdir -p $expdir/vocab

echo "learning BPE"
cat $train_file.SRC  $train_file.TGT > $train_file.ALL
python $SUBWORD_NMT_DIR/subword_nmt/learn_bpe.py \
   --input $train_file.ALL \
   -s $num_operations \
   -o $expdir/vocab/bpe_codes.32k.SRC_TGT \
   --num-workers -1 

echo "computing SRC vocab"
python $SUBWORD_NMT_DIR/subword_nmt/apply_bpe.py \
    -c $expdir/vocab/bpe_codes.32k.SRC_TGT \
    --num-workers -1  \
    -i $train_file.SRC  | \
python $SUBWORD_NMT_DIR/subword_nmt/get_vocab.py \
    > $expdir/vocab/vocab.tmp.SRC
python clean_vocab.py $expdir/vocab/vocab.tmp.SRC $expdir/vocab/vocab.SRC
#rm $expdir/vocab/vocab.tmp.SRC

echo "computing TGT vocab"
python $SUBWORD_NMT_DIR/subword_nmt/apply_bpe.py \
    -c $expdir/vocab/bpe_codes.32k.SRC_TGT \
    --num-workers -1  \
    -i $train_file.TGT  | \
python $SUBWORD_NMT_DIR/subword_nmt/get_vocab.py \
    > $expdir/vocab/vocab.tmp.TGT
python clean_vocab.py $expdir/vocab/vocab.tmp.TGT $expdir/vocab/vocab.TGT
#rm $expdir/vocab/vocab.tmp.TGT

rm $train_file.ALL

