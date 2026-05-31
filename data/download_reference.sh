#!/bin/bash
# Download chr21 reference genome (hg38)
# Run from repo root

set -euo pipefail

mkdir -p data/ref

echo "[1/3] Downloading chr21 reference..."
wget -q --show-progress \
  "https://hgdownload.soe.ucsc.edu/goldenPath/hg38/chromosomes/chr21.fa.gz" \
  -O data/ref/chr21.fa.gz

echo "[2/3] Decompressing..."
gunzip data/ref/chr21.fa.gz

echo "[3/3] Indexing..."
samtools faidx data/ref/chr21.fa
gatk CreateSequenceDictionary -R data/ref/chr21.fa

echo "Reference ready: data/ref/chr21.fa"
