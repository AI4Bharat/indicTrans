import sys
import codecs

def clean_vocab(in_vocab_fname, out_vocab_fname):
    with codecs.open(in_vocab_fname, "r", encoding="utf-8") as infile, codecs.open(
        out_vocab_fname, "w", encoding="utf-8"
    ) as outfile:
        for i, line in enumerate(infile):
            fields = line.strip("\r\n ").split(" ")
            if len(fields) == 2:
                outfile.write(line)
            if len(fields) != 2:
                print("{}: {}".format(i, line.strip()))
                for c in line:
                    print("{}:{}".format(c, hex(ord(c))))


if __name__ == "__main__":
    clean_vocab(sys.argv[1], sys.argv[2])
