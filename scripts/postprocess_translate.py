INDIC_NLP_LIB_HOME = "indic_nlp_library"
INDIC_NLP_RESOURCES = "indic_nlp_resources"
import sys

from indicnlp import transliterate

sys.path.append(r"{}".format(INDIC_NLP_LIB_HOME))
from indicnlp import common

common.set_resources_path(INDIC_NLP_RESOURCES)
from indicnlp import loader

loader.load()
from sacremoses import MosesPunctNormalizer
from sacremoses import MosesTokenizer
from sacremoses import MosesDetokenizer
from collections import defaultdict

import indicnlp
from indicnlp.tokenize import indic_tokenize
from indicnlp.tokenize import indic_detokenize
from indicnlp.normalize import indic_normalize
from indicnlp.transliterate import unicode_transliterate


def postprocess(
    infname, outfname, input_size, lang, common_lang="hi", transliterate=False
):
    """
    parse fairseq interactive output, convert script back to native Indic script (in case of Indic languages) and detokenize.

    infname: fairseq log file
    outfname: output file of translation (sentences not translated contain the dummy string 'DUMMY_OUTPUT'
    input_size: expected number of output sentences
    lang: language
    """

    consolidated_testoutput = []
    # with open(infname,'r',encoding='utf-8') as infile:
    # consolidated_testoutput= list(map(lambda x: x.strip(), filter(lambda x: x.startswith('H-'),infile) ))
    # consolidated_testoutput.sort(key=lambda x: int(x.split('\t')[0].split('-')[1]))
    # consolidated_testoutput=[ x.split('\t')[2] for x in consolidated_testoutput ]

    consolidated_testoutput = [(x, 0.0, "") for x in range(input_size)]
    temp_testoutput = []
    with open(infname, "r", encoding="utf-8") as infile:
        temp_testoutput = list(
            map(
                lambda x: x.strip().split("\t"),
                filter(lambda x: x.startswith("H-"), infile),
            )
        )
        temp_testoutput = list(
            map(lambda x: (int(x[0].split("-")[1]), float(x[1]), x[2]), temp_testoutput)
        )
        for sid, score, hyp in temp_testoutput:
            consolidated_testoutput[sid] = (sid, score, hyp)
        consolidated_testoutput = [x[2] for x in consolidated_testoutput]

    if lang == "en":
        en_detok = MosesDetokenizer(lang="en")
        with open(outfname, "w", encoding="utf-8") as outfile:
            for sent in consolidated_testoutput:
                outfile.write(en_detok.detokenize(sent.split(" ")) + "\n")
    else:
        xliterator = unicode_transliterate.UnicodeIndicTransliterator()
        with open(outfname, "w", encoding="utf-8") as outfile:
            for sent in consolidated_testoutput:
                if transliterate:
                    outstr = indic_detokenize.trivial_detokenize(
                        xliterator.transliterate(sent, common_lang, lang), lang
                    )
                else:
                    outstr = indic_detokenize.trivial_detokenize(sent, lang)
                outfile.write(outstr + "\n")


if __name__ == "__main__":
    #     # The path to the local git repo for Indic NLP library
    # INDIC_NLP_LIB_HOME="indic_nlp_library"
    # INDIC_NLP_RESOURCES = "indic_nlp_resources"
    # sys.path.append('{}'.format(INDIC_NLP_LIB_HOME))
    # common.set_resources_path(INDIC_NLP_RESOURCES)
    #     # The path to the local git repo for Indic NLP Resources
    #     INDIC_NLP_RESOURCES=""

    #     sys.path.append('{}'.format(INDIC_NLP_LIB_HOME))
    #     common.set_resources_path(INDIC_NLP_RESOURCES)

    # loader.load()

    infname = sys.argv[1]
    outfname = sys.argv[2]
    input_size = int(sys.argv[3])
    lang = sys.argv[4]
    if len(sys.argv) == 5:
        transliterate = False
    elif len(sys.argv) == 6:
        transliterate = sys.argv[5]
        if transliterate.lower() == "true":
            transliterate = True
        else:
            transliterate = False
    else:
        print(f"Invalid arguments: {sys.argv}")
        exit()

    postprocess(
        infname, outfname, input_size, lang, common_lang="hi", transliterate=transliterate
    )
