exp_dir=$1
src_lang=$2
tgt_lang=$3

train_data_dir=$exp_dir/raw_data/train/$src_lang-$tgt_lang/
devtest_data_dir=$exp_dir/raw_data/devtest/$src_lang-$tgt_lang/

train_processed_dir=$exp_dir/data/
devtest_processed_dir=$exp_dir/data/

out_data_dir=$exp_dir/final_bin

mkdir -p $train_processed_dir
mkdir -p $devtest_processed_dir
mkdir -p $out_data_dir

# train preprocessing
$train_infname_src=$train_data_dir/train.$src_lang
$train_infname_tgt=$train_data_dir/train.$tgt_lang
$train_outfname_src=$train_processed_dir/train.SRC
$train_outfname_tgt=$train_processed_dir/train.TGT
echo "Applying normalization and script conversion for train"
input_size=`python preprocess_translate.py $train_infname_src $train_outfname_src $src_lang`
input_size=`python preprocess_translate.py $train_outfname_src $train_outfname_tgt $tgt_lang`
echo "Number of sentences in train: $input_size"

# dev preprocessing
$dev_infname_src=$devtest_data_dir/dev.$src_lang
$dev_infname_tgt=$devtest_data_dir/dev.$tgt_lang
$dev_outfname_src=$devtest_processed_dir/dev.SRC
$dev_outfname_tgt=$devtest_processed_dir/dev.TGT
echo "Applying normalization and script conversion for dev"
input_size=`python preprocess_translate.py $dev_infname_src $dev_outfname_src $src_lang`
input_size=`python preprocess_translate.py $dev_outfname_src $dev_outfname_tgt $tgt_lang`
echo "Number of sentences in dev: $input_size"

# test preprocessing
$test_infname_src=$devtest_data_dir/test.$src_lang
$test_infname_tgt=$devtest_data_dir/test.$tgt_lang
$test_outfname_src=$devtest_processed_dir/test.SRC
$test_outfname_tgt=$devtest_processed_dir/test.TGT
echo "Applying normalization and script conversion for test"
input_size=`python preprocess_translate.py $test_infname_src $test_outfname_src $src_lang`
input_size=`python preprocess_translate.py $test_outfname_src $test_outfname_tgt $tgt_lang`
echo "Number of sentences in test: $input_size"

echo "Learning bpe. This will take a very long time"
# learn bpe for preprocessed_train files
bash learn_bpe.sh $exp_dir

echo "Applying bpe"
bash apply_bpe_traindevtest_notag.sh $exp_dir

# this is only required for joint training
# echo "Adding language tags"
# python add_tags_translate.py $outfname._bpe $outfname.bpe $src_lang $tgt_lang

echo "Binarizing data"
bash binarize_training_exp.sh $exp_dir SRC TGT
