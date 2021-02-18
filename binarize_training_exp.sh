#/bin/bash 

source $PYTHON_ENV/bin/activate

exp_dir=$1
src_lang=$2
tgt_lang=$3

`dirname $0`/env.sh

data_dir=$exp_dir/final
out_data_dir=$exp_dir/final_bin

rm -rf $out_data_dir

fairseq-preprocess \
    --source-lang $src_lang --target-lang $tgt_lang \
    --trainpref $data_dir/train \
    --validpref $data_dir/dev \
    --testpref $data_dir/test \
    --destdir $out_data_dir \
    --workers 30    
