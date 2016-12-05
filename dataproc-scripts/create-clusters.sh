#!/bin/bash
gcloud dataproc clusters create gs1-sample \
    --project irnlp-gs1 \
    --bucket irnlp-gs1 \
    --initialization-actions \
        gs://irnlp-gs1/scripts/dataproc-init/mecab.sh