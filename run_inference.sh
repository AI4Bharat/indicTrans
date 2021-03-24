src_lang=${1:-hi}
tgt_lang=${2:-en}

mkdir -p ../baselines
expdir=../baselines/baselines-${src_lang}-${tgt_lang}

if [[ -d $expdir ]]
then
    echo "$expdir exists on your filesystem."
else
    cd ../baselines
	gsutil -m cp -r gs://mt-datasets/baseline_experiments/baselines-${src_lang}-${tgt_lang} .
	cd ../indicTrans
fi





if [ $src_lang == 'hi' ] || [ $tgt_lang == 'hi' ]; then
	TEST_SETS=( wmt-news wat2021-devtest wat2020-devtest anuvaad-legal tico19 sap-documentation-benchmark all)
elif [ $src_lang == 'ta' ] || [ $tgt_lang == 'ta' ]; then
	TEST_SETS=( wmt-news wat2021-devtest wat2020-devtest anuvaad-legal  tico19 all)
elif [ $src_lang == 'bn' ] || [ $tgt_lang == 'bn' ]; then
	TEST_SETS=( wat2021-devtest wat2020-devtest anuvaad-legal tico19 all)
elif [ $src_lang == 'gu' ] || [ $tgt_lang == 'gu' ]; then
	TEST_SETS=( wmt-news wat2021-devtest wat2020-devtest all)
elif [ $src_lang == 'as' ] || [ $tgt_lang == 'as' ]; then
	TEST_SETS=( all )
elif [ $src_lang == 'kn' ] || [ $tgt_lang == 'kn' ]; then
	TEST_SETS=( wat2021-devtest anuvaad-legal all)
elif [ $src_lang == 'ml' ] || [ $tgt_lang == 'ml' ]; then
	TEST_SETS=( wat2021-devtest wat2020-devtest anuvaad-legal all)
elif [ $src_lang == 'mr' ] || [ $tgt_lang == 'mr' ]; then
	TEST_SETS=( wat2021-devtest wat2020-devtest all)
elif [ $src_lang == 'or' ] || [ $tgt_lang == 'or' ]; then
	TEST_SETS=( all )
elif [ $src_lang == 'pa' ] || [ $tgt_lang == 'pa' ]; then
	TEST_SETS=( all )
elif [ $src_lang == 'te' ] || [ $tgt_lang == 'te' ]; then
	TEST_SETS=( anuvaad-legal wat2020-devtest wat2021-devtest all )
fi

if [ $src_lang == 'en' ]; then
	indic_lang=$tgt_lang
else
	indic_lang=$src_lang
fi


for tset in ${TEST_SETS[@]};do
	echo $tset $src_lang $tgt_lang
	if [ $tset == 'wat2021-devtest' ]; then
		SRC_FILE=${expdir}/devtest/$tset/test.$src_lang
		REF_FILE=${expdir}/devtest/$tset/test.$tgt_lang
	else
		SRC_FILE=${expdir}/devtest/$tset/en-${indic_lang}/test.$src_lang
		REF_FILE=${expdir}/devtest/$tset/en-${indic_lang}/test.$tgt_lang
	fi
	RESULTS_DIR=${expdir}/results/$tset

	mkdir -p $RESULTS_DIR

	bash translate.sh $SRC_FILE $RESULTS_DIR/${src_lang}-${tgt_lang} $src_lang $tgt_lang $expdir $REF_FILE
	# for newline between different outputs
	echo
done
