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
    ROLE=$(curl -f -s -H Metadata-Flavor:Google http://metadata/computeMetadata/v1/instance/attributes/dataproc-role)
    INIT_ACTIONS_REPO=$(curl -f -s -H Metadata-Flavor:Google http://metadata/computeMetadata/v1/instance/attributes/INIT_ACTIONS_REPO || true)
    INIT_ACTIONS_REPO="${INIT_ACTIONS_REPO:-https://github.com/GoogleCloudPlatform/dataproc-initialization-actions.git}"
    INIT_ACTIONS_BRANCH=$(curl -f -s -H Metadata-Flavor:Google http://metadata/computeMetadata/v1/instance/attributes/INIT_ACTIONS_BRANCH || true)
    INIT_ACTIONS_BRANCH="${INIT_ACTIONS_BRANCH:-master}"
    DATAPROC_BUCKET=$(curl -f -s -H Metadata-Flavor:Google http://metadata/computeMetadata/v1/instance/attributes/dataproc-bucket)

    echo "Cloning fresh dataproc-initialization-actions from repo $INIT_ACTIONS_REPO and branch $INIT_ACTIONS_BRANCH..."
    cd $TEMP_DIR
    git clone -b "$INIT_ACTIONS_BRANCH" --single-branch $INIT_ACTIONS_REPO
    # Install Miniconda / conda
    ./dataproc-initialization-actions/conda/bootstrap-conda.sh
    # install mecab for python
    pip install mecab-python3
}

# run
init
mecab-ko
mecab-ko-dic
mecab-python