from tqdm import tqdm
import sys


def remove_large_sentences(src_path, tgt_path):
    count = 0
    new_src_lines = []
    new_tgt_lines = []
    src_num_lines = sum(1 for line in open(src_path, "r", encoding="utf-8"))
    tgt_num_lines = sum(1 for line in open(tgt_path, "r", encoding="utf-8"))
    assert src_num_lines == tgt_num_lines
    with open(src_path, encoding="utf-8") as f1, open(tgt_path, encoding="utf-8") as f2:
        for src_line, tgt_line in tqdm(zip(f1, f2), total=src_num_lines):
            src_tokens = src_line.strip().split(" ")
            tgt_tokens = tgt_line.strip().split(" ")
            if len(src_tokens) > 200 or len(tgt_tokens) > 200:
                count += 1
                continue
            new_src_lines.append(src_line)
            new_tgt_lines.append(tgt_line)
    return count, new_src_lines, new_tgt_lines


def create_txt(outFile, lines, add_newline=False):
    outfile = open("{0}".format(outFile), "w", encoding="utf-8")
    for line in lines:
        if add_newline:
            outfile.write(line + "\n")
        else:
            outfile.write(line)
    outfile.close()


if __name__ == "__main__":

    src_path = sys.argv[1]
    tgt_path = sys.argv[2]
    new_src_path = sys.argv[3]
    new_tgt_path = sys.argv[4]

    count, new_src_lines, new_tgt_lines = remove_large_sentences(src_path, tgt_path)
    print(f'{count} lines removed due to seq_len > 200')
    create_txt(new_src_path, new_src_lines)
    create_txt(new_tgt_path, new_tgt_lines)
