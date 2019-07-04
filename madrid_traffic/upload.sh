#!/bin/sh
gcloud builds submit --tag gcr.io/tinybirdtest/madrid_traffic && gcloud beta run deploy --image gcr.io/tinybirdtest/madrid_traffic
