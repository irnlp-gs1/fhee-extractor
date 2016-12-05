#!/usr/bin/env bash
set -e

MECAB_KO_FNAME=mecab-0.996-ko-0.9.2
MECAB_KO_URL=https://bitbucket.org/eunjeon/mecab-ko/downloads/$MECAB_KO_FNAME.tar.gz
MECAB_KO_DIC_FNAME=mecab-ko-dic-2.0.1-20150920
MECAB_KO_DIC_URL=https://bitbucket.org/eunjeon/mecab-ko-dic/downloads/$MECAB_KO_DIC_FNAME.tar.gz

mkdir -p /tmp
TEMP_DIR=/tmp

init() {
    apt-get install -y build-essential autoconf automake libtool
}

mecab-ko() {
    echo "Installing mecab-ko"
    wget -O $TEMP_DIR/mecab-ko.tar.gz $MECAB_KO_URL
    tar xzf $TEMP_DIR/mecab-ko.tar.gz -C $TEMP_DIR 
    cd $TEMP_DIR/$MECAB_KO_FNAME
    ./configure && make && make install
}

mecab-ko-dic() {
    echo "Installing mecab-ko-dic"
    wget -O $TEMP_DIR/mecab-ko-dic.tar.gz $MECAB_KO_DIC_URL
    tar xzf $TEMP_DIR/mecab-ko-dic.tar.gz -C $TEMP_DIR
    cd $TEMP_DIR/$MECAB_KO_DIC_FNAME
    ldconfig && ./autogen.sh && ./configure && make && make install
}

mecab-python() {
    # Install Miniconda / conda
    ./dataproc-initialization-actions/conda/bootstrap-conda.sh
    # Update conda root environment with specific packages in pip and conda
    CONDA_PACKAGES=''
    PIP_PACKAGES='mecab-python3'
    CONDA_PACKAGES=$CONDA_PACKAGES PIP_PACKAGES=$PIP_PACKAGES ./dataproc-initialization-actions/conda/install-conda-env.sh
}

# run
init
mecab-ko
mecab-ko-dic
# mecab-python