import sys
from indicnlp import common   
from indicnlp import loader

from sacremoses import MosesPunctNormalizer
from sacremoses import MosesTokenizer
from sacremoses import MosesDetokenizer
from collections import defaultdict

from tqdm import tqdm

import indicnlp
from indicnlp.tokenize import indic_tokenize
from indicnlp.tokenize import indic_detokenize
from indicnlp.normalize import indic_normalize
from indicnlp.transliterate import unicode_transliterate

def preprocess(infname,outfname,lang,common_lang='hi'):
    """
    Normalize, tokenize and script convert(for Indic)
    return number of sentences input file 
    
    """
    
    n=0
    num_lines = sum(1 for line in open(infname,'r'))
    ### reading 
    with open(infname,'r',encoding='utf-8') as infile, \
         open(outfname,'w',encoding='utf-8') as outfile:
        

        if lang=='en':
            en_tok=MosesTokenizer(lang='en')
            en_normalizer = MosesPunctNormalizer()
            for line in tqdm(infile, total=num_lines): 
                outline=' '.join(
                        en_tok.tokenize( 
                                en_normalizer.normalize(line.strip()), 
                                    escape=False ) )
                outfile.write(outline+'\n')
                n=n+1
                
        else:
            normfactory=indic_normalize.IndicNormalizerFactory()
            normalizer=normfactory.get_normalizer(lang)
            for line in tqdm(infile, total=num_lines): 

                line=indic_detokenize.trivial_detokenize(line.strip(),lang)

                outline=unicode_transliterate.UnicodeIndicTransliterator.transliterate(
                        ' '.join(
                                    indic_tokenize.trivial_tokenize(
                                         normalizer.normalize(line.strip()),   lang) ), lang, common_lang)


                outfile.write(outline+'\n')
                n=n+1
                
    return n
                
if __name__ == '__main__':
#     # The path to the local git repo for Indic NLP library
#     INDIC_NLP_LIB_HOME=r"/data/t-ankunc/installs/indic_nlp_library_py3"

#     # The path to the local git repo for Indic NLP Resources
#     INDIC_NLP_RESOURCES=r"/data/t-ankunc/installs/indic_nlp_resources"

#     sys.path.append(r'{}'.format(INDIC_NLP_LIB_HOME))
#     common.set_resources_path(INDIC_NLP_RESOURCES)

    loader.load()    
    
    infname=sys.argv[1]
    outfname=sys.argv[2]
    lang=sys.argv[3]
    
    print(preprocess(infname,outfname,lang))
