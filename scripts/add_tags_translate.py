import sys


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


if __name__ == '__main__':

    infname = sys.argv[1]
    outfname = sys.argv[2]
    src_lang = sys.argv[3]
    tgt_lang = sys.argv[4]

    with open(infname, 'r', encoding='utf-8') as infile, \
            open(outfname, 'w', encoding='utf-8') as outfile:
        for line in infile:
            outstr = add_token(
                line.strip(), [('src', src_lang), ('tgt', tgt_lang)])
            outfile.write(outstr + '\n')
