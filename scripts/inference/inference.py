INDIC_NLP_LIB_HOME = "indic_nlp_library"
INDIC_NLP_RESOURCES = "indic_nlp_resources"
import sys

sys.path.append(r"{}".format(INDIC_NLP_LIB_HOME))
from indicnlp import common

common.set_resources_path(INDIC_NLP_RESOURCES)
from indicnlp import loader

loader.load()
from sacremoses import MosesPunctNormalizer
from sacremoses import MosesTokenizer
from sacremoses import MosesDetokenizer
from collections import defaultdict
import codecs
from fairseq.models.transformer import TransformerModel

from tqdm import tqdm
from joblib import Parallel, delayed

from indicnlp.tokenize import indic_tokenize
from indicnlp.tokenize import indic_detokenize
from indicnlp.normalize import indic_normalize
from indicnlp.transliterate import unicode_transliterate

from subword_nmt.apply_bpe import BPE, read_vocabulary

expdir = "../experiments/all-v1_WAT/"
en_tok = MosesTokenizer(lang="en")
en_normalizer = MosesPunctNormalizer()
vocabulary = read_vocabulary(
    codecs.open(f"{expdir}/vocab/vocab.SRC", encoding="utf-8"), 5
)
bpe = BPE(
    codecs.open(f"{expdir}/vocab/bpe_codes.32k.SRC_TGT", encoding="utf-8"),
    -1,
    "@@",
    vocabulary,
    None,
)

# model = TransformerModel.from_pretrained(
#     "experiments/all-v1_WAT/model",
#     checkpoint_file="checkpoint_best.pt",
#     data_name_or_path="experiments/all-v1_WAT/final_bin",
#     bpe=None,
#     bpe_codes="experiments/all-v1_WAT/vocab/bpe_codes.32k.SRC_TGT",
# )


def add_token(sent, tag_infos):
    """add special tokens specified by tag_infos to each element in list

    tag_infos: list of tuples (tag_type,tag)

    each tag_info results in a token of the form: __{tag_type}__{tag}__

    """

    tokens = []
    for tag_type, tag in tag_infos:
        token = "__" + tag_type + "__" + tag + "__"
        tokens.append(token)

    return " ".join(tokens) + " " + sent


def preprocess_sent(sent, normalizer, lang):
    if lang == "en":
        return " ".join(
            en_tok.tokenize(en_normalizer.normalize(sent.strip()), escape=False)
        )
    else:
        # line = indic_detokenize.trivial_detokenize(line.strip(), lang)
        return unicode_transliterate.UnicodeIndicTransliterator.transliterate(
            " ".join(
                indic_tokenize.trivial_tokenize(
                    normalizer.normalize(sent.strip()), lang
                )
            ),
            lang,
            "hi",
        ).replace(" ् ", "्")


def preprocess(sents, lang):
    """
    Normalize, tokenize and script convert(for Indic)
    return number of sentences input file

    """

    if lang == "en":

        # processed_sents = Parallel(n_jobs=-1, backend="multiprocessing")(
        #     delayed(preprocess_line)(line, None, lang) for line in tqdm(sents, total=num_lines)
        # )
        processed_sents = [preprocess_sent(line, None, lang) for line in tqdm(sents)]

    else:
        normfactory = indic_normalize.IndicNormalizerFactory()
        normalizer = normfactory.get_normalizer(lang)

        # processed_sents = Parallel(n_jobs=-1, backend="multiprocessing")(
        #     delayed(preprocess_line)(line, normalizer, lang) for line in tqdm(infile, total=num_lines)
        # )
        processed_sents = [
            preprocess_sent(line, normalizer, lang) for line in tqdm(sents)
        ]

    return processed_sents


def apply_lang_tags(sents, src_lang, tgt_lang):
    tagged_sents = []
    for sent in sents:
        tagged_sent = add_token(sent.strip(), [("src", src_lang), ("tgt", tgt_lang)])
        tagged_sents.append(tagged_sent)
    return tagged_sents


def postprocess(sents, lang, common_lang="hi"):
    """
    parse fairseq interactive output, convert script back to native Indic script (in case of Indic languages) and detokenize.

    infname: fairseq log file
    outfname: output file of translation (sentences not translated contain the dummy string 'DUMMY_OUTPUT'
    input_size: expected number of output sentences
    lang: language
    """
    postprocessed_sents = []

    if lang == "en":
        en_detok = MosesDetokenizer(lang="en")
        for sent in sents:
            # outfile.write(en_detok.detokenize(sent.split(" ")) + "\n")
            postprocessed_sents.append(en_detok.detokenize(sent.split(" ")))
    else:
        xliterator = unicode_transliterate.UnicodeIndicTransliterator()
        for sent in sents:
            outstr = indic_detokenize.trivial_detokenize(
                xliterator.transliterate(sent, common_lang, lang), lang
            )
            # outfile.write(outstr + "\n")
            postprocessed_sents.append(outstr)
    return postprocessed_sents


def apply_bpe(sents):

    return [bpe.process_line(sent) for sent in sents]


if __name__ == "__main__":
    tgt_lang = "en"
    src_lang = "hi"
    sents = []

    preprocessed_sents = preprocess(sents, lang=src_lang)
    bpe_sents = apply_bpe(preprocessed_sents)
    tagged_sents = apply_lang_tags(bpe_sents, src_lang, tgt_lang)

    translations = model.translate(tagged_sents, beam=5)
    postprocessed_sents = postprocess(translations, tgt_lang)
