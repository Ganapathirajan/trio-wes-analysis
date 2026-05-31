#!/bin/bash
# Tool installation for Google Colab
# Run this cell first in Colab

set -euo pipefail

echo "=== Installing samtools + bcftools ==="
apt-get update -qq
apt-get install -y samtools bcftools tabix 2>&1 | tail -3

echo "=== Installing GATK 4.4.0.0 ==="
wget -q https://github.com/broadinstitute/gatk/releases/download/4.4.0.0/gatk-4.4.0.0.zip
unzip -q gatk-4.4.0.0.zip
ln -sf /content/gatk-4.4.0.0/gatk /usr/local/bin/gatk

echo "=== Installing slivar 0.3.0 ==="
wget -q https://github.com/brentp/slivar/releases/download/v0.3.0/slivar
chmod +x slivar
mv slivar /usr/local/bin/slivar

echo "=== Verifying tools ==="
samtools --version | head -1
bcftools --version | head -1
gatk --version
slivar 2>&1 | head -1

echo "=== All tools ready ==="
