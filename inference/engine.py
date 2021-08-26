from os import truncate
from sacremoses import MosesPunctNormalizer
from sacremoses import MosesTokenizer
from sacremoses import MosesDetokenizer
from subword_nmt.apply_bpe import BPE, read_vocabulary
import codecs
from tqdm import tqdm
from indicnlp.tokenize import indic_tokenize
from indicnlp.tokenize import indic_detokenize
from indicnlp.normalize import indic_normalize
from indicnlp.transliterate import unicode_transliterate
from mosestokenizer import MosesSentenceSplitter
from indicnlp.tokenize import sentence_tokenize

from inference.custom_interactive import Translator


INDIC = ["as", "bn", "gu", "hi", "kn", "ml", "mr", "or", "pa", "ta", "te"]


def split_sentences(paragraph, language):
    if language == "en":
        with MosesSentenceSplitter(language) as splitter:
            return splitter([paragraph])
    elif language in INDIC:
        return sentence_tokenize.sentence_split(paragraph, lang=language)


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


def apply_lang_tags(sents, src_lang, tgt_lang):
    tagged_sents = []
    for sent in sents:
        tagged_sent = add_token(sent.strip(), [("src", src_lang), ("tgt", tgt_lang)])
        tagged_sents.append(tagged_sent)
    return tagged_sents


def truncate_long_sentences(sents):

    MAX_SEQ_LEN = 200
    new_sents = []

    for sent in sents:
        words = sent.split()
        num_words = len(words)
        if num_words > MAX_SEQ_LEN:
            print_str = " ".join(words[:5]) + " .... " + " ".join(words[-5:])
            sent = " ".join(words[:MAX_SEQ_LEN])
            print(
                f"WARNING: Sentence {print_str} truncated to 200 tokens as it exceeds maximum length limit"
            )

        new_sents.append(sent)
    return new_sents


class Model:
    def __init__(self, expdir):
        self.expdir = expdir
        self.en_tok = MosesTokenizer(lang="en")
        self.en_normalizer = MosesPunctNormalizer()
        self.en_detok = MosesDetokenizer(lang="en")
        self.xliterator = unicode_transliterate.UnicodeIndicTransliterator()
        print("Initializing vocab and bpe")
        self.vocabulary = read_vocabulary(
            codecs.open(f"{expdir}/vocab/vocab.SRC", encoding="utf-8"), 5
        )
        self.bpe = BPE(
            codecs.open(f"{expdir}/vocab/bpe_codes.32k.SRC", encoding="utf-8"),
            -1,
            "@@",
            self.vocabulary,
            None,
        )

        print("Initializing model for translation")
        # initialize the model
        self.translator = Translator(
            f"{expdir}/final_bin", f"{expdir}/model/checkpoint_best.pt", batch_size=100
        )

    # translate a batch of sentences from src_lang to tgt_lang
    def batch_translate(self, batch, src_lang, tgt_lang):

        assert isinstance(batch, list)
        preprocessed_sents = self.preprocess(batch, lang=src_lang)
        bpe_sents = self.apply_bpe(preprocessed_sents)
        tagged_sents = apply_lang_tags(bpe_sents, src_lang, tgt_lang)
        tagged_sents = truncate_long_sentences(tagged_sents)

        translations = self.translator.translate(tagged_sents)
        postprocessed_sents = self.postprocess(translations, tgt_lang)

        return postprocessed_sents

    # translate a paragraph from src_lang to tgt_lang
    def translate_paragraph(self, paragraph, src_lang, tgt_lang):

        assert isinstance(paragraph, str)
        sents = split_sentences(paragraph, src_lang)

        postprocessed_sents = self.batch_translate(sents, src_lang, tgt_lang)

        translated_paragraph = " ".join(postprocessed_sents)

        return translated_paragraph

    def preprocess_sent(self, sent, normalizer, lang):
        if lang == "en":
            return " ".join(
                self.en_tok.tokenize(
                    self.en_normalizer.normalize(sent.strip()), escape=False
                )
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

    def preprocess(self, sents, lang):
        """
        Normalize, tokenize and script convert(for Indic)
        return number of sentences input file

        """

        if lang == "en":

            # processed_sents = Parallel(n_jobs=-1, backend="multiprocessing")(
            #     delayed(preprocess_line)(line, None, lang) for line in tqdm(sents, total=num_lines)
            # )
            processed_sents = [
                self.preprocess_sent(line, None, lang) for line in tqdm(sents)
            ]

        else:
            normfactory = indic_normalize.IndicNormalizerFactory()
            normalizer = normfactory.get_normalizer(lang)

            # processed_sents = Parallel(n_jobs=-1, backend="multiprocessing")(
            #     delayed(preprocess_line)(line, normalizer, lang) for line in tqdm(infile, total=num_lines)
            # )
            processed_sents = [
                self.preprocess_sent(line, normalizer, lang) for line in tqdm(sents)
            ]

        return processed_sents

    def postprocess(self, sents, lang, common_lang="hi"):
        """
        parse fairseq interactive output, convert script back to native Indic script (in case of Indic languages) and detokenize.

        infname: fairseq log file
        outfname: output file of translation (sentences not translated contain the dummy string 'DUMMY_OUTPUT'
        input_size: expected number of output sentences
        lang: language
        """
        postprocessed_sents = []

        if lang == "en":
            for sent in sents:
                # outfile.write(en_detok.detokenize(sent.split(" ")) + "\n")
                postprocessed_sents.append(self.en_detok.detokenize(sent.split(" ")))
        else:
            for sent in sents:
                outstr = indic_detokenize.trivial_detokenize(
                    self.xliterator.transliterate(sent, common_lang, lang), lang
                )
                # outfile.write(outstr + "\n")
                postprocessed_sents.append(outstr)
        return postprocessed_sents

    def apply_bpe(self, sents):

        return [self.bpe.process_line(sent) for sent in sents]
