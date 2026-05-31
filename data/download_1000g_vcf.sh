#!/bin/bash
# Download 1000 Genomes Phase 3 chr21 VCF
# Run from repo root

set -euo pipefail

mkdir -p data/vcf

echo "Downloading 1000G chr21 VCF (~200MB)..."
wget -q --show-progress \
  "https://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/ALL.chr21.phase3_shapeit2_mvncall_integrated_v5b.20130502.genotypes.vcf.gz" \
  -O data/vcf/1000g_chr21.vcf.gz

echo "Indexing..."
tabix -p vcf data/vcf/1000g_chr21.vcf.gz

echo "VCF ready: data/vcf/1000g_chr21.vcf.gz"
echo "Samples in VCF: $(bcftools query -l data/vcf/1000g_chr21.vcf.gz | wc -l)"
