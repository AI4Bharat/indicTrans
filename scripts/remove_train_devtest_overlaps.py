import os
import string
import shutil
from itertools import permutations, chain
from collections import defaultdict
from tqdm import tqdm
import sys

INDIC_LANGS = ["as", "bn", "gu", "hi", "kn", "ml", "mr", "or", "pa", "ta", "te"]
# we will be testing the overlaps of training data with all these benchmarks
# benchmarks = ['wat2021-devtest', 'wat2020-devtest', 'wat-2018', 'wmt-news', 'ufal-ta', 'pmi']


def read_lines(path):
    # if path doesnt exist, return empty list
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        lines = f.readlines()
    return lines


def create_txt(outFile, lines):
    add_newline = not "\n" in lines[0]
    outfile = open("{0}".format(outFile), "w")
    for line in lines:
        if add_newline:
            outfile.write(line + "\n")
        else:
            outfile.write(line)

    outfile.close()


def pair_dedup_files(src_file, tgt_file):
    src_lines = read_lines(src_file)
    tgt_lines = read_lines(tgt_file)
    len_before = len(src_lines)

    src_dedupped, tgt_dedupped = pair_dedup_lists(src_lines, tgt_lines)

    len_after = len(src_dedupped)
    num_duplicates = len_before - len_after

    print(f"Dropped duplicate pairs in {src_file} Num duplicates -> {num_duplicates}")
    create_txt(src_file, src_dedupped)
    create_txt(tgt_file, tgt_dedupped)


def pair_dedup_lists(src_list, tgt_list):
    src_tgt = list(set(zip(src_list, tgt_list)))
    src_deduped, tgt_deduped = zip(*src_tgt)
    return src_deduped, tgt_deduped


def strip_and_normalize(line):
    # lowercase line, remove spaces and strip punctuation

    # one of the fastest way to add an exclusion list and remove that
    # list of characters from a string
    # https://towardsdatascience.com/how-to-efficiently-remove-punctuations-from-a-string-899ad4a059fb
    exclist = string.punctuation + "\u0964"
    table_ = str.maketrans("", "", exclist)

    line = line.replace(" ", "").lower()
    # dont use this method, it is painfully slow
    # line = "".join([i for i in line if i not in string.punctuation])
    line = line.translate(table_)
    return line


def expand_tupled_list(list_of_tuples):
    # convert list of tuples into two lists
    # https://stackoverflow.com/questions/8081545/how-to-convert-list-of-tuples-to-multiple-lists
    # [(en, as), (as, bn), (bn, gu)] - > [en, as, bn], [as, bn, gu]
    list_a, list_b = map(list, zip(*list_of_tuples))
    return list_a, list_b


def get_src_tgt_lang_lists(many2many=False):
    if many2many is False:
        SRC_LANGS = ["en"]
        TGT_LANGS = INDIC_LANGS
    else:
        all_languages = INDIC_LANGS + ["en"]
        # lang_pairs = list(permutations(all_languages, 2))

        SRC_LANGS, TGT_LANGS = all_languages, all_languages

    return SRC_LANGS, TGT_LANGS


def normalize_and_gather_all_benchmarks(devtest_dir, many2many=False):

    # This is a dict of dict of lists
    # the first keys are for lang-pair, the second keys are for src/tgt
    # the values are the devtest lines.
    # so devtest_pairs_normalized[en-as][src] will store src(en lines)
    # so devtest_pairs_normalized[en-as][tgt] will store tgt(as lines)
    devtest_pairs_normalized = defaultdict(lambda: defaultdict(list))
    SRC_LANGS, TGT_LANGS = get_src_tgt_lang_lists(many2many)
    benchmarks = os.listdir(devtest_dir)
    for dataset in benchmarks:
        for src_lang in SRC_LANGS:
            for tgt_lang in TGT_LANGS:
                if src_lang == tgt_lang:
                    continue
                if dataset == "wat2021-devtest":
                    # wat2021 dev and test sets have differnet folder structure
                    src_dev = read_lines(f"{devtest_dir}/{dataset}/dev.{src_lang}")
                    tgt_dev = read_lines(f"{devtest_dir}/{dataset}/dev.{tgt_lang}")
                    src_test = read_lines(f"{devtest_dir}/{dataset}/test.{src_lang}")
                    tgt_test = read_lines(f"{devtest_dir}/{dataset}/test.{tgt_lang}")
                else:
                    src_dev = read_lines(
                        f"{devtest_dir}/{dataset}/{src_lang}-{tgt_lang}/dev.{src_lang}"
                    )
                    tgt_dev = read_lines(
                        f"{devtest_dir}/{dataset}/{src_lang}-{tgt_lang}/dev.{tgt_lang}"
                    )
                    src_test = read_lines(
                        f"{devtest_dir}/{dataset}/{src_lang}-{tgt_lang}/test.{src_lang}"
                    )
                    tgt_test = read_lines(
                        f"{devtest_dir}/{dataset}/{src_lang}-{tgt_lang}/test.{tgt_lang}"
                    )

                # if the tgt_pair data doesnt exist for a particular test set,
                # it will be an empty list
                if tgt_test == [] or tgt_dev == []:
                    # print(f'{dataset} does not have {src_lang}-{tgt_lang} data')
                    continue

                # combine both dev and test sets into one
                src_devtest = src_dev + src_test
                tgt_devtest = tgt_dev + tgt_test

                src_devtest = [strip_and_normalize(line) for line in src_devtest]
                tgt_devtest = [strip_and_normalize(line) for line in tgt_devtest]

                devtest_pairs_normalized[f"{src_lang}-{tgt_lang}"]["src"].extend(
                    src_devtest
                )
                devtest_pairs_normalized[f"{src_lang}-{tgt_lang}"]["tgt"].extend(
                    tgt_devtest
                )

    # dedup merged benchmark datasets
    for src_lang in SRC_LANGS:
        for tgt_lang in TGT_LANGS:
            if src_lang == tgt_lang:
                continue
            src_devtest, tgt_devtest = (
                devtest_pairs_normalized[f"{src_lang}-{tgt_lang}"]["src"],
                devtest_pairs_normalized[f"{src_lang}-{tgt_lang}"]["tgt"],
            )
            # if the devtest data doesnt exist for the src-tgt pair then continue
            if src_devtest == [] or tgt_devtest == []:
                continue
            src_devtest, tgt_devtest = pair_dedup_lists(src_devtest, tgt_devtest)
            (
                devtest_pairs_normalized[f"{src_lang}-{tgt_lang}"]["src"],
                devtest_pairs_normalized[f"{src_lang}-{tgt_lang}"]["tgt"],
            ) = (
                src_devtest,
                tgt_devtest,
            )

    return devtest_pairs_normalized


def remove_train_devtest_overlaps(train_dir, devtest_dir, many2many=False):

    devtest_pairs_normalized = normalize_and_gather_all_benchmarks(
        devtest_dir, many2many
    )

    SRC_LANGS, TGT_LANGS = get_src_tgt_lang_lists(many2many)

    if not many2many:
        all_src_sentences_normalized = []
        for key in devtest_pairs_normalized:
            all_src_sentences_normalized.extend(devtest_pairs_normalized[key]["src"])
        # remove all duplicates. Now this contains all the normalized
        # english sentences in all test benchmarks across all lang pair
        all_src_sentences_normalized = list(set(all_src_sentences_normalized))
    else:
        all_src_sentences_normalized = None

    src_overlaps = []
    tgt_overlaps = []
    for src_lang in SRC_LANGS:
        for tgt_lang in TGT_LANGS:
            if src_lang == tgt_lang:
                continue
            new_src_train = []
            new_tgt_train = []

            pair = f"{src_lang}-{tgt_lang}"
            src_train = read_lines(f"{train_dir}/{pair}/train.{src_lang}")
            tgt_train = read_lines(f"{train_dir}/{pair}/train.{tgt_lang}")

            len_before = len(src_train)
            if len_before == 0:
                continue

            src_train_normalized = [strip_and_normalize(line) for line in src_train]
            tgt_train_normalized = [strip_and_normalize(line) for line in tgt_train]

            if all_src_sentences_normalized:
                src_devtest_normalized = all_src_sentences_normalized
            else:
                src_devtest_normalized = devtest_pairs_normalized[pair]["src"]

            tgt_devtest_normalized = devtest_pairs_normalized[pair]["tgt"]

            # compute all src and tgt super strict overlaps for a lang pair
            overlaps = set(src_train_normalized) & set(src_devtest_normalized)
            src_overlaps.extend(list(overlaps))

            overlaps = set(tgt_train_normalized) & set(tgt_devtest_normalized)
            tgt_overlaps.extend(list(overlaps))
            # dictionaries offer o(1) lookup
            src_overlaps_dict = {}
            tgt_overlaps_dict = {}
            for line in src_overlaps:
                src_overlaps_dict[line] = 1
            for line in tgt_overlaps:
                tgt_overlaps_dict[line] = 1

            # loop to remove the ovelapped data
            idx = -1
            for src_line_norm, tgt_line_norm in tqdm(
                zip(src_train_normalized, tgt_train_normalized), total=len_before
            ):
                idx += 1
                if src_overlaps_dict.get(src_line_norm, None):
                    continue
                if tgt_overlaps_dict.get(tgt_line_norm, None):
                    continue
                new_src_train.append(src_train[idx])
                new_tgt_train.append(tgt_train[idx])

            len_after = len(new_src_train)
            print(
                f"Detected overlaps between train and devetest for {pair} is {len_before - len_after}"
            )
            print(f"saving new files at {train_dir}/{pair}/")
            create_txt(f"{train_dir}/{pair}/train.{src_lang}", new_src_train)
            create_txt(f"{train_dir}/{pair}/train.{tgt_lang}", new_tgt_train)


if __name__ == "__main__":
    train_data_dir = sys.argv[1]
    # benchmarks directory should contains all the test sets
    devtest_data_dir = sys.argv[2]
    if len(sys.argv) == 3:
        many2many = False
    elif len(sys.argv) == 4:
        many2many = sys.argv[4]
        if many2many.lower() == "true":
            many2many = True
        else:
            many2many = False
    remove_train_devtest_overlaps(train_data_dir, devtest_data_dir, many2many)
