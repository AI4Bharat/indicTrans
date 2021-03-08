#!/bin/bash

expdir=$1  # EXPDIR
org_data_dir=$2
langs=$3

#`dirname $0`/env.sh
SUBWORD_NMT_DIR="subword-nmt"
echo "Apply to each language"

for dset in `echo test dev`
do 
    echo $dset 

    in_dset_dir="$org_data_dir/$dset"
    out_dset_dir="$expdir/bpe/$dset"

    for lang in $langs
    do 

        echo Apply BPE for $dset "-" $lang 
    
        mkdir -p $out_dset_dir 
    
        python $SUBWORD_NMT_DIR/subword_nmt/apply_bpe.py \
            -c $expdir/vocab/bpe_codes.32k.SRC_TGT \
            --vocabulary $expdir/vocab/vocab.SRC \
            --vocabulary-threshold 5 \
            < $in_dset_dir/$dset.$lang \
            > $out_dset_dir/$dset.$lang 

    done 
done 
