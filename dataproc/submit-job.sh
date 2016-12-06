#!/bin/bash
gcloud dataproc jobs submit pyspark --async --cluster gs1-fhee hello-world.py