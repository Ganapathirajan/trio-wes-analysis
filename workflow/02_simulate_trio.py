#!/usr/bin/env python3
"""
02_simulate_trio.py
Simulate trio VCF (PROBAND + MOTHER + FATHER) from a single-sample VCF.

Strategy:
  - Het variants in proband → randomly assigned to one parent (45%) or the other (45%)
    or neither (~10% = simulated de novo)
  - Hom alt variants → both parents het (recessive model)
  - Hom ref → both parents ref

Input:  data/vcf/NA12878_chr21.vcf.gz
Output: data/vcf/trio_synthetic.vcf.gz

Usage:
    python workflow/02_simulate_trio.py
"""

import gzip
import os
import random
import subprocess

random.seed(42)  # Reproducible

IN_VCF  = "data/vcf/NA12878_chr21.vcf.gz"
OUT_VCF = "data/vcf/trio_synthetic.vcf"

os.makedirs("data/vcf", exist_ok=True)

print(f"Reading: {IN_VCF}")
print("Simulating trio genotypes (seed=42)...")

with gzip.open(IN_VCF, "rt") as fin, open(OUT_VCF, "w") as fout:
    for line in fin:
        # Pass meta-info lines unchanged
        if line.startswith("##"):
            fout.write(line)
            continue

        # Update sample header
        if line.startswith("#CHROM"):
            fout.write(line.strip().replace("NA12878", "PROBAND") + "\tMOTHER\tFATHER\n")
            continue

        parts = line.strip().split("\t")
        proband_gt = parts[9]
        gt = proband_gt.split(":")[0]
        rest = ":" + ":".join(proband_gt.split(":")[1:]) if ":" in proband_gt else ""

        if gt in ("0/1", "0|1", "1|0"):
            r = random.random()
            if r < 0.45:        # inherited from mother
                mom_gt = "0/1" + rest
                dad_gt = "0/0" + rest
            elif r < 0.90:      # inherited from father
                mom_gt = "0/0" + rest
                dad_gt = "0/1" + rest
            else:               # de novo (~10%)
                mom_gt = "0/0" + rest
                dad_gt = "0/0" + rest

        elif gt in ("1/1", "1|1"):  # homozygous recessive
            mom_gt = "0/1" + rest
            dad_gt = "0/1" + rest

        else:  # hom ref or other
            mom_gt = proband_gt
            dad_gt = proband_gt

        parts[9] = proband_gt
        fout.write("\t".join(parts) + f"\t{mom_gt}\t{dad_gt}\n")

print(f"Compressing {OUT_VCF}...")
subprocess.run(["bgzip", "-f", OUT_VCF], check=True)
subprocess.run(["tabix", "-p", "vcf", OUT_VCF + ".gz"], check=True)

# Verify
result = subprocess.run(
    ["bcftools", "query", "-l", OUT_VCF + ".gz"],
    capture_output=True, text=True
)
print("Samples:", result.stdout.strip().split("\n"))

result2 = subprocess.run(
    ["bcftools", "stats", OUT_VCF + ".gz"],
    capture_output=True, text=True
)
for line in result2.stdout.splitlines():
    if line.startswith("SN"):
        print(line)

print(f"\nDone: {OUT_VCF}.gz")
