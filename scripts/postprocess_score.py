import sys

def postprocess(
    infname, outfname, input_size
):
    """
    parse fairseq interactive output, convert script back to native Indic script (in case of Indic languages) and detokenize.

    infname: fairseq log file
    outfname: output file of translation (sentences not translated contain the dummy string 'DUMMY_OUTPUT'
    input_size: expected number of output sentences
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
        #consolidated_testoutput = [x[2] for x in consolidated_testoutput]

    with open(outfname, "w", encoding="utf-8") as outfile:
        for (sid, score, hyp) in consolidated_testoutput:
            outfile.write("{}\n".format(score))

if __name__ == "__main__":

    infname = sys.argv[1]
    outfname = sys.argv[2]
    input_size = int(sys.argv[3])

    postprocess(
        infname, outfname, input_size
    )
