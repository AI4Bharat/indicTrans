import sys
from tqdm import tqdm
import os


def add_token(sent, tag_infos):
    """ add special tokens specified by tag_infos to each element in list

    tag_infos: list of tuples (tag_type,tag)

    each tag_info results in a token of the form: __{tag_type}__{tag}__

    """

    tokens = []
    for tag_type, tag in tag_infos:
        token = '__' + tag_type + '__' + tag + '__'
        tokens.append(token)

    return ' '.join(tokens) + ' ' + sent


def generate_lang_tag_iterator(infname):
    with open(infname, 'r', encoding='utf-8') as infile:
        for line in infile:
            src, tgt, count = line.strip().split('\t')
            count = int(count)
            for _ in range(count):
                yield (src, tgt)


if __name__ == '__main__':

    expdir = sys.argv[1]
    dset = sys.argv[2]

    src_fname = '{expdir}/bpe/{dset}.SRC'.format(
        expdir=expdir, dset=dset)
    tgt_fname = '{expdir}/bpe/{dset}.TGT'.format(
        expdir=expdir, dset=dset)
    meta_fname = '{expdir}/data/{dset}_lang_pairs.txt'.format(
        expdir=expdir, dset=dset)

    out_src_fname = '{expdir}/final/{dset}.SRC'.format(
        expdir=expdir, dset=dset)
    out_tgt_fname = '{expdir}/final/{dset}.TGT'.format(
        expdir=expdir, dset=dset)
    lang_tag_iterator = generate_lang_tag_iterator(meta_fname)

    os.makedirs('{expdir}/final'.format(expdir=expdir), exist_ok=True)

    with open(src_fname, 'r', encoding='utf-8') as srcfile, \
            open(tgt_fname, 'r', encoding='utf-8') as tgtfile, \
            open(out_src_fname, 'w', encoding='utf-8') as outsrcfile, \
            open(out_tgt_fname, 'w', encoding='utf-8') as outtgtfile:

        for (l1, l2), src_sent, tgt_sent in tqdm(zip(lang_tag_iterator,
                                                     srcfile, tgtfile)):
            outsrcfile.write(add_token(src_sent.strip(), [
                             ('src', l1), ('tgt', l2)]) + '\n')
            outtgtfile.write(tgt_sent.strip() + '\n')
