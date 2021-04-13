from tqdm import tqdm
import os
from collections import defaultdict


def read_file(fname):
    with open(fname, "r", encoding="utf-8") as infile:
        for line in infile:
            yield line.strip()


def extract_non_english_pairs(indir, outdir, LANGS):
    """
    Extracts non-english pair parallel corpora

    indir: contains english centric data in the following form:
            - directory named en-xx for language xx
            - each directory contains a train.en and train.xx
    outdir: output directory to store mined data for each pair.
            One directory is created for each pair.
    LANGS: list of languages in the corpus (other than English).
            The language codes must correspond to the ones used in the
            files and directories in indir. Prefarably, sort the languages
            in this list in alphabetic order. outdir will contain data for xx-yy,
            but not for yy-xx, so it will be convenient to have this list in sorted order.
    """

    for i in tqdm(range(len(LANGS) - 1)):
        print()
        for j in range(i + 1, len(LANGS)):
            lang1 = LANGS[i]
            lang2 = LANGS[j]
            #         print()
            print("{} {}".format(lang1, lang2))

            fname1 = "{}/en-{}/train.en".format(indir, lang1)
            fname2 = "{}/en-{}/train.en".format(indir, lang2)
            #         print(fname1)
            #         print(fname2)
            enset_l1 = set(read_file(fname1))
            common_en_set = enset_l1.intersection(read_file(fname2))

            ## this block should be used if you want to consider multiple translations.
            # il_fname1 = "{}/en-{}/train.{}".format(indir, lang1, lang1)
            # en_lang1_dict = defaultdict(list)
            # for en_line, il_line in zip(read_file(fname1), read_file(il_fname1)):
            #     if en_line in common_en_set:
            #         en_lang1_dict[en_line].append(il_line)

            #         # this block should be used if you DONT to consider multiple translation.
            il_fname1='{}/en-{}/train.{}'.format(indir,lang1,lang1)
            en_lang1_dict={}
            for en_line,il_line in zip(read_file(fname1),read_file(il_fname1)):
                if en_line in common_en_set:
                    en_lang1_dict[en_line]=il_line

            os.makedirs("{}/{}-{}".format(outdir, lang1, lang2), exist_ok=True)
            out_l1_fname = "{o}/{l1}-{l2}/train.{l1}".format(
                o=outdir, l1=lang1, l2=lang2
            )
            out_l2_fname = "{o}/{l1}-{l2}/train.{l2}".format(
                o=outdir, l1=lang1, l2=lang2
            )

            il_fname2 = "{}/en-{}/train.{}".format(indir, lang2, lang2)
            with open(out_l1_fname, "w", encoding="utf-8") as out_l1_file, open(
                out_l2_fname, "w", encoding="utf-8"
            ) as out_l2_file:
                for en_line, il_line in zip(read_file(fname2), read_file(il_fname2)):
                    if en_line in en_lang1_dict:

                        # this block should be used if you want to consider multiple tranlations.
                        for il_line_lang1 in en_lang1_dict[en_line]:
                        #     lang1_line, lang2_line = il_line_lang1, il_line
                        #     out_l1_file.write(lang1_line + "\n")
                        #     out_l2_file.write(lang2_line + "\n")

                    # this block should be used if you DONT to consider multiple translation.
	                        lang1_line, lang2_line = en_lang1_dict[en_line], il_line
	                        out_l1_file.write(lang1_line+'\n')
	                        out_l2_file.write(lang2_line+'\n')


def get_extracted_stats(outdir, LANGS):
    """
    gathers stats from the extracted directories

    outdir: output directory to store mined data for each pair.
            One directory is created for each pair.
    LANGS: list of languages in the corpus (other than languages).
            The language codes must correspond to the ones used in the
            files and directories in indir. Prefarably, sort the languages
            in this list in alphabetic order. outdir will contain data for xx-yy,
    """
    common_stats = []
    for i in tqdm(range(len(LANGS) - 1)):
        for j in range(i + 1, len(LANGS)):
            lang1 = LANGS[i]
            lang2 = LANGS[j]

            out_l1_fname = "{o}/{l1}-{l2}/train.{l1}".format(
                o=outdir, l1=lang1, l2=lang2
            )

            cnt = sum([1 for _ in read_file(out_l1_fname)])
            common_stats.append((lang1, lang2, cnt))
            common_stats.append((lang2, lang1, cnt))
    return common_stats
