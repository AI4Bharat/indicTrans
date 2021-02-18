#NVIDIA CUDA download 
wget "https://developer.nvidia.com/compute/cuda/10.0/Prod/local_installers/cuda_10.0.130_410.48_linux"
wget "http://developer.download.nvidia.com/compute/cuda/10.0/Prod/patches/1/cuda_10.0.130.1_linux.run"

## do not install drivers (See this: https://docs.nvidia.com/deploy/cuda-compatibility/index.html)
sudo sh "cuda_10.0.130_410.48_linux"
sudo sh "cuda_10.0.130.1_linux.run"

#Set environment variables 
export CUDA_HOME=/usr/local/cuda-10.0
export PATH=$CUDA_HOME/bin:$PATH
export LD_LIBRARY_PATH=$CUDA_HOME/lib64:$LD_LIBRARY_PATH

# Install pytorch 1.2 
python3 -m venv  pytorch1.2
source pytorch1.2/bin/activate
which pip3
pip3 install torch==1.2.0 torchvision==0.4.0

# Install nccl 
git clone https://github.com/NVIDIA/nccl.git
cd nccl
make src.build CUDA_HOME=$CUDA_HOME
sudo apt install build-essential devscripts debhelper fakeroot
make pkg.debian.build CUDA_HOME=$CUDA_HOME
sudo dpkg -i build/pkg/deb/libnccl2_2.7.8-1+cuda10.0_amd64.deb
sudo dpkg -i build/pkg/deb/libnccl-dev_2.7.8-1+cuda10.0_amd64.deb
sudo apt-get install -f

# Install Apex 
git clone https://github.com/NVIDIA/apex
cd apex
pip install -v --no-cache-dir --global-option="--cpp_ext" --global-option="--cuda_ext" \
  --global-option="--deprecated_fused_adam" --global-option="--xentropy" \
  --global-option="--fast_multihead_attn" ./

# Install PyArrow 
pip install pyarrow

# Install fairseq 
pip install --editable ./

# Install other dependencies 
pip install sacrebleu 
pip install tensorboardX --user
