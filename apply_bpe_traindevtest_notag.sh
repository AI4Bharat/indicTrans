#!/bin/bash

expdir=$1  # EXPDIR

SUBWORD_NMT_DIR="subword-nmt"

data_dir="$expdir/data"
mkdir -p $expdir/bpe

for dset in `echo train dev test`
do
    echo $dset
    in_dset_dir="$data_dir/$dset"
    out_dset_dir="$expdir/bpe/$dset"
    # out_dset_dir="$expdir/final/$dset"
    echo "Apply to SRC corpus"
    python $SUBWORD_NMT_DIR/subword_nmt/apply_bpe.py \
        -c $expdir/vocab/bpe_codes.32k.SRC_TGT \
        --vocabulary $expdir/vocab/vocab.SRC \
        --vocabulary-threshold 5 \
        --num-workers "-1" \
        < $in_dset_dir.SRC \
        > $out_dset_dir.SRC
    echo "Apply to TGT corpus"
    python $SUBWORD_NMT_DIR/subword_nmt/apply_bpe.py \
        -c $expdir/vocab/bpe_codes.32k.SRC_TGT \
        --vocabulary $expdir/vocab/vocab.TGT \
        --vocabulary-threshold 5 \
        --num-workers "-1" \
        < $in_dset_dir.TGT \
        > $out_dset_dir.TGT
done
