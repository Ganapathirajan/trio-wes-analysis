#!/bin/bash
# Extract NA12878 from 1000G VCF (chr21 only)
# Input:  data/vcf/1000g_chr21.vcf.gz
# Output: data/vcf/NA12878_chr21.vcf.gz

set -euo pipefail

mkdir -p data/vcf

echo "[1/2] Extracting NA12878, filtering to PASS biallelic SNPs..."
bcftools view \
  -s NA12878 \
  -m2 -M2 -v snps \
  -f PASS \
  data/vcf/1000g_chr21.vcf.gz \
  -O z -o data/vcf/NA12878_chr21.vcf.gz

echo "[2/2] Indexing..."
tabix -p vcf data/vcf/NA12878_chr21.vcf.gz

echo "Done."
echo "Variant count:"
bcftools stats data/vcf/NA12878_chr21.vcf.gz | grep "^SN" | head -5
