#!/bin/bash
# 03_slivar_inheritance.sh
# Apply inheritance model filters using slivar
#
# Input:  data/vcf/trio_synthetic.vcf.gz + data/trio.ped
# Output: results/slivar/trio_inherited.vcf.gz
#
# Models applied:
#   denovo    — proband het, both parents hom_ref
#   recessive — proband hom_alt, both parents het
#   x_linked  — proband hom_alt, mother het, father hom_ref

set -euo pipefail

mkdir -p results/slivar

echo "=== Running slivar inheritance filtering ==="

slivar expr \
  --vcf  data/vcf/trio_synthetic.vcf.gz \
  --ped  data/trio.ped \
  --pass-only \
  --trio "denovo:kid.het && mom.hom_ref && dad.hom_ref" \
  --trio "recessive:kid.hom_alt && mom.het && dad.het" \
  --trio "x_linked:kid.hom_alt && mom.het && dad.hom_ref" \
  -o results/slivar/trio_inherited.vcf

bgzip -f results/slivar/trio_inherited.vcf
tabix -p vcf results/slivar/trio_inherited.vcf.gz

echo ""
echo "=== Variant counts by inheritance model ==="
bcftools stats results/slivar/trio_inherited.vcf.gz | grep "^SN"

echo ""
echo "Done: results/slivar/trio_inherited.vcf.gz"
