expdir=${1:-../experiments/all-v1_WAT}
lang=${2:-hi}

bash translate.sh ../experiments/devtest/anuvaad-legal/en-$lang/test.$lang $expdir/results/anuvaad-legal/en-$lang $lang "en" $expdir ../experiments/devtest/anuvaad-legal/en-$lang/test.en
bash translate.sh ../experiments/devtest/wmt-news/en-$lang/test.$lang $expdir/results/wmt-news/en-$lang $lang "en" $expdir ../experiments/devtest/wmt-news/en-$lang/test.en
bash translate.sh ../experiments/devtest/wat2021/test.$lang $expdir/results/wat2021/en-$lang $lang "en" $expdir ../experiments/devtest/wat2021/test.en
bash translate.sh ../experiments/devtest/wat2020/en-$lang/test.$lang $expdir/results/wat2020/en-$lang $lang "en" $expdir ../experiments/devtest/wat2020/en-$lang/test.en
bash translate.sh ../experiments/devtest/tico19/en-$lang/test.$lang $expdir/results/tico19/en-$lang $lang "en" $expdir ../experiments/devtest/tico19/en-$lang/test.en
bash translate.sh ../experiments/devtest/sap-documentation-benchmark/en-$lang/test.$lang $expdir/results/sap-documentation-benchmark/en-$lang $lang "en" $expdir ../experiments/devtest/sap-documentation-benchmark/en-$lang/test.en
bash translate.sh ../experiments/devtest/all/en-$lang/test.$lang $expdir/results/all/en-$lang $lang "en" $expdir ../experiments/devtest/all/en-$lang/test.en

