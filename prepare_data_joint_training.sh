exp_dir=$1
src_lang=$2
tgt_lang=$3
vocab_type=${4:-"sep"} # sep or joint
train_data_dir=${5:-"$exp_dir"}
devtest_data_dir=${6:-"$exp_dir/devtest/all"}

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
	# this is for preprocessing text and in for indic langs, we convert all scripts to devnagiri
	input_size=`python scripts/preprocess_translate.py $train_infname_src $train_outfname_src $src_lang true`
	input_size=`python scripts/preprocess_translate.py $train_infname_tgt $train_outfname_tgt $tgt_lang true`
	echo "Number of sentences in train: $input_size"

	# dev preprocessing
	dev_infname_src=$devtest_data_dir/en-${lang}/dev.$src_lang
	dev_infname_tgt=$devtest_data_dir/en-${lang}/dev.$tgt_lang
	dev_outfname_src=$devtest_norm_dir/dev.$src_lang
	dev_outfname_tgt=$devtest_norm_dir/dev.$tgt_lang
	echo "Applying normalization and script conversion for dev"
	input_size=`python scripts/preprocess_translate.py $dev_infname_src $dev_outfname_src $src_lang true`
	input_size=`python scripts/preprocess_translate.py $dev_infname_tgt $dev_outfname_tgt $tgt_lang true`
	echo "Number of sentences in dev: $input_size"

	# test preprocessing
	test_infname_src=$devtest_data_dir/en-${lang}/test.$src_lang
	test_infname_tgt=$devtest_data_dir/en-${lang}/test.$tgt_lang
	test_outfname_src=$devtest_norm_dir/test.$src_lang
	test_outfname_tgt=$devtest_norm_dir/test.$tgt_lang
	echo "Applying normalization and script conversion for test"
	input_size=`python scripts/preprocess_translate.py $test_infname_src $test_outfname_src $src_lang true`
	input_size=`python scripts/preprocess_translate.py $test_infname_tgt $test_outfname_tgt $tgt_lang true`
	echo "Number of sentences in test: $input_size"
done
# this concatenates lang pair data and creates text files to keep track of number of lines in each lang pair.
# this is imp as for joint training, we will merge all the lang pairs and the indivitual lang lines info
# would be required for adding specific lang tags later.

# the outputs of these scripts will  be text file like this:
# <lang1> <lang2> <number of lines>
# lang1-lang2 n1
# lang1-lang3 n2

python scripts/concat_joint_data.py $exp_dir/norm $exp_dir/data $src_lang $tgt_lang 'train'
python scripts/concat_joint_data.py $exp_dir/norm $exp_dir/data $src_lang $tgt_lang 'dev'
python scripts/concat_joint_data.py $exp_dir/norm $exp_dir/data $src_lang $tgt_lang 'test'

# echo "Learning bpe. This will take a very long time depending on the size of the dataset"
echo `date`
# # learn bpe for preprocessed_train files
# for creating joint_vocab use this
# bash learn_bpe.sh $exp_dir

# for sep vocab use this
# bash learn_single_bpe.sh $exp_dir
# check if vocab type is single
if [[ "$vocab_type" == "sep" ]]
then
    bash learn_single_bpe.sh $exp_dir
else 
    bash learn_bpe.sh $exp_dir
fi

echo `date`



# echo "Applying bpe"
# apply the learnt bpe to the data for joint vocab
# bash apply_bpe_traindevtest_notag.sh $exp_dir
# apply the learnt bpe to the data for sep vocab
# bash apply_single_bpe_traindevtest_notag.sh $exp_dir

if [[ "$vocab_type" == "sep" ]]
then
    bash apply_single_bpe_traindevtest_notag.sh $exp_dir
else 
    bash apply_bpe_traindevtest_notag.sh $exp_dir
fi

mkdir -p $exp_dir/final

# # this is only required for joint training
# we apply language tags to the bpe segmented data
#
# if we are translating lang1 to lang2 then <lang1 line> will become __src__ <lang1> __tgt__ <lang2> <lang1 line>
echo "Adding language tags"
python scripts/add_joint_tags_translate.py $exp_dir 'train'
python scripts/add_joint_tags_translate.py $exp_dir 'dev'
python scripts/add_joint_tags_translate.py $exp_dir 'test'

# # this is important step if you are training with tpu and using num_batch_buckets
# # the currnet implementation does not remove outliers before bucketing and hence
# # removing these large sentences ourselves helps with getting better buckets
# python scripts/remove_large_sentences.py $exp_dir/bpe/train.SRC $exp_dir/bpe/train.TGT $exp_dir/final/train.SRC $exp_dir/final/train.TGT
# python scripts/remove_large_sentences.py $exp_dir/bpe/dev.SRC $exp_dir/bpe/dev.TGT $exp_dir/final/dev.SRC $exp_dir/final/dev.TGT
# python scripts/remove_large_sentences.py $exp_dir/bpe/test.SRC $exp_dir/bpe/test.TGT $exp_dir/final/test.SRC $exp_dir/final/test.TGT

# echo "Binarizing data"
# Binarize the training data for using with fairseq train
bash binarize_training_exp.sh $exp_dir SRC TGT
