
export SRC=''

## Python env directory where fairseq is installed 
export PYTHON_ENV=''

export SUBWORD_NMT_DIR=''
export INDIC_RESOURCES_PATH=''
export INDIC_NLP_HOME=''

export CUDA_HOME=''

export PATH=$CUDA_HOME/bin:$INDIC_NLP_HOME:$PATH
export LD_LIBRARY_PATH=$CUDA_HOME/lib64

# set environment variable to control GPUS visible to the application 
#export CUDA_VISIBLE_DEVICES="'
