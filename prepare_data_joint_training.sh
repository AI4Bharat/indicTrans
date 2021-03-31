exp_dir=$1
src_lang=$2
tgt_lang=$3
train_data_dir=${4:-"$exp_dir"}
devtest_data_dir=${5:-"$exp_dir/devtest/all"}

echo "Running experiment ${exp_dir} on ${src_lang} to ${tgt_lang}"


train_processed_dir=$exp_dir/data
devtest_processed_dir=$exp_dir/data

out_data_dir=$exp_dir/final_bin

mkdir -p $train_processed_dir
mkdir -p $devtest_processed_dir
mkdir -p $out_data_dir
langs=(as bn hi gu kn ml mr or pa ta te)

for lang in ${langs[@]};do
	if [ $src_lang == en ]; then
		tgt_lang=$lang
	else
		src_lang=$lang
	fi

	train_norm_dir=$exp_dir/norm/$src_lang-$tgt_lang
	devtest_norm_dir=$exp_dir/norm/$src_lang-$tgt_lang
	mkdir -p $train_norm_dir
	mkdir -p $devtest_norm_dir

	# train preprocessing
	train_infname_src=$train_data_dir/en-${lang}/train.$src_lang
	train_infname_tgt=$train_data_dir/en-${lang}/train.$tgt_lang
	train_outfname_src=$train_norm_dir/train.$src_lang
	train_outfname_tgt=$train_norm_dir/train.$tgt_lang
	echo "Applying normalization and script conversion for train"
	input_size=`python preprocess_translate.py $train_infname_src $train_outfname_src $src_lang true`
	input_size=`python preprocess_translate.py $train_infname_tgt $train_outfname_tgt $tgt_lang true`
	echo "Number of sentences in train: $input_size"

	# dev preprocessing
	dev_infname_src=$devtest_data_dir/en-${lang}/dev.$src_lang
	dev_infname_tgt=$devtest_data_dir/en-${lang}/dev.$tgt_lang
	dev_outfname_src=$devtest_norm_dir/dev.$src_lang
	dev_outfname_tgt=$devtest_norm_dir/dev.$tgt_lang
	echo "Applying normalization and script conversion for dev"
	input_size=`python preprocess_translate.py $dev_infname_src $dev_outfname_src $src_lang true`
	input_size=`python preprocess_translate.py $dev_infname_tgt $dev_outfname_tgt $tgt_lang true`
	echo "Number of sentences in dev: $input_size"

	# test preprocessing
	test_infname_src=$devtest_data_dir/en-${lang}/test.$src_lang
	test_infname_tgt=$devtest_data_dir/en-${lang}/test.$tgt_lang
	test_outfname_src=$devtest_norm_dir/test.$src_lang
	test_outfname_tgt=$devtest_norm_dir/test.$tgt_lang
	echo "Applying normalization and script conversion for test"
	input_size=`python preprocess_translate.py $test_infname_src $test_outfname_src $src_lang true`
	input_size=`python preprocess_translate.py $test_infname_tgt $test_outfname_tgt $tgt_lang true`
	echo "Number of sentences in test: $input_size"
done

python concat_joint_data.py $exp_dir/norm $exp_dir/data $src_lang $tgt_lang 'train'
python concat_joint_data.py $exp_dir/norm $exp_dir/data $src_lang $tgt_lang 'dev'
python concat_joint_data.py $exp_dir/norm $exp_dir/data $src_lang $tgt_lang 'test'

# echo "Learning bpe. This will take a very long time depending on the size of the dataset"
echo `date`
# # learn bpe for preprocessed_train files
bash learn_bpe.sh $exp_dir
echo `date`

# echo "Applying bpe"
bash apply_bpe_traindevtest_notag.sh $exp_dir

mkdir -p $exp_dir/final

# # this is only required for joint training
echo "Adding language tags"
python add_joint_tags_translate.py $exp_dir 'train'
python add_joint_tags_translate.py $exp_dir 'dev'
python add_joint_tags_translate.py $exp_dir 'test'

# # this is imporatnt step if you are training with tpu and using num_batch_buckets
# # the currnet implementation does not remove outliers before bucketing and hence
# # removing these large sentences ourselves helps with getting better buckets
# python remove_large_sentences.py $exp_dir/bpe/train.SRC $exp_dir/bpe/train.TGT $exp_dir/final/train.SRC $exp_dir/final/train.TGT
# python remove_large_sentences.py $exp_dir/bpe/dev.SRC $exp_dir/bpe/dev.TGT $exp_dir/final/dev.SRC $exp_dir/final/dev.TGT
# python remove_large_sentences.py $exp_dir/bpe/test.SRC $exp_dir/bpe/test.TGT $exp_dir/final/test.SRC $exp_dir/final/test.TGT

# echo "Binarizing data"
bash binarize_training_exp.sh $exp_dir SRC TGT
