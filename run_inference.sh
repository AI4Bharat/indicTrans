expdir=${1:-../experiments/all-v1_WAT}
src_lang=${2:-hi}
tgt_lang=${3:-en}


if [ $src_lang == 'hi' ] || [ $tgt_lang == 'hi' ]; then
	TEST_SETS=( anuvaad-legal wmt-news wat2021 wat2020 tico19 sap-documentation-benchmark all)
elif [ $src_lang == 'ta' ] || [ $tgt_lang == 'ta' ]; then
	TEST_SETS=( anuvaad-legal wmt-news wat2021 wat2020 tico19 all)
elif [ $src_lang == 'bn' ] || [ $tgt_lang == 'bn' ]; then
	TEST_SETS=( anuvaad-legal wat2021 wat2020 tico19 all)
fi


for tset in ${TEST_SETS[@]};do
	echo $tset $src_lang $tgt_lang
	if [ $tset == 'wat2021' ]; then
		SRC_FILE=../experiments/devtest/$tset/test.$src_lang
		REF_FILE=../experiments/devtest/$tset/test.$tgt_lang
	else
		SRC_FILE=../experiments/devtest/$tset/${tgt_lang}-${src_lang}/test.$src_lang
		REF_FILE=../experiments/devtest/$tset/${tgt_lang}-${src_lang}/test.$tgt_lang
	fi
	RESULTS_DIR=$expdir/results/$tset

	mkdir -p $RESULTS_DIR

	bash translate.sh $SRC_FILE $RESULTS_DIR/${src_lang}-${tgt_lang} $src_lang $tgt_lang $expdir $REF_FILE
done


