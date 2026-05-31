#!/usr/bin/env python3
"""
04_vep_annotation.py
Annotate slivar candidate variants using Ensembl VEP REST API (batch mode).
Filters to HIGH and MODERATE impact variants only.

Input:  results/slivar/trio_inherited.vcf.gz
Output: results/annotated/coding_candidates.csv
        results/annotated/all_candidates.tsv

Requirements: requests, pandas, bcftools (on PATH)

Usage:
    python workflow/04_vep_annotation.py
"""

import json
import os
import subprocess
import time

import pandas as pd
import requests

# ── Config ──────────────────────────────────────────────────────────────────
IN_VCF   = "results/slivar/trio_inherited.vcf.gz"
OUT_DIR  = "results/annotated"
OUT_TSV  = f"{OUT_DIR}/all_candidates.tsv"
OUT_CSV  = f"{OUT_DIR}/coding_candidates.csv"

VEP_URL     = "https://rest.ensembl.org/vep/human/region"
BATCH_SIZE  = 200
SLEEP_SEC   = 0.3
IMPACT_KEEP = {"HIGH", "MODERATE"}

os.makedirs(OUT_DIR, exist_ok=True)


# ── Step 1: Extract all candidates to TSV ───────────────────────────────────
print("[1/3] Extracting candidates from VCF...")
subprocess.run(
    f"bcftools query -f '%CHROM\\t%POS\\t%REF\\t%ALT\\t%INFO/denovo\\t%INFO/recessive\\n' "
    f"{IN_VCF} > {OUT_TSV}",
    shell=True, check=True
)

df = pd.read_csv(OUT_TSV, sep="\t", header=None,
                 names=["CHROM", "POS", "REF", "ALT", "DENOVO", "RECESSIVE"])
df["CHROM"] = df["CHROM"].astype(str)
print(f"  Total candidates: {len(df)}")


# ── Step 2: VEP batch annotation ────────────────────────────────────────────
def vep_batch(chunk: pd.DataFrame) -> list:
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    variants = [
        f"{row.CHROM} {row.POS} . {row.REF} {row.ALT} . . ."
        for _, row in chunk.iterrows()
    ]
    payload = json.dumps({"variants": variants})
    try:
        r = requests.post(VEP_URL, headers=headers, data=payload, timeout=30)
        if r.status_code == 200:
            return r.json()
        else:
            print(f"  API {r.status_code}: {r.text[:100]}")
    except Exception as e:
        print(f"  Exception: {e}")
    return []


print(f"[2/3] Annotating {len(df)} variants via VEP REST API (batch={BATCH_SIZE})...")
results = []

for i in range(0, len(df), BATCH_SIZE):
    chunk = df.iloc[i:i + BATCH_SIZE]
    batch_results = vep_batch(chunk)

    for res in batch_results:
        for tc in res.get("transcript_consequences", []):
            impact = tc.get("impact", "")
            if impact in IMPACT_KEEP:
                results.append({
                    "CHROM":       res.get("seq_region_name"),
                    "POS":         res.get("start"),
                    "GENE":        tc.get("gene_symbol", "."),
                    "CONSEQUENCE": tc.get("consequence_terms", ["."])[0],
                    "IMPACT":      impact,
                    "HGVSc":       tc.get("hgvsc", "."),
                    "HGVSp":       tc.get("hgvsp", "."),
                    "SIFT":        tc.get("sift_prediction", "."),
                    "BIOTYPE":     tc.get("biotype", "."),
                    "MOST_SEVERE": res.get("most_severe_consequence", "."),
                    "COLOCATED":   str(res.get("colocated_variants", [{}])[0].get("id", ".")),
                })

    time.sleep(SLEEP_SEC)
    if i % 4000 == 0:
        print(f"  {i}/{len(df)} processed — coding hits: {len(results)}")

coding = pd.DataFrame(results).drop_duplicates(subset=["CHROM", "POS", "GENE"])
coding["CHROM"] = coding["CHROM"].astype(str)
coding["POS"]   = coding["POS"].astype(int)

print(f"  Total coding candidates: {len(coding)}")


# ── Step 3: Merge inheritance model ─────────────────────────────────────────
print("[3/3] Merging inheritance model labels...")
df["POS"] = df["POS"].astype(int)

merged = coding.merge(df[["CHROM", "POS", "DENOVO", "RECESSIVE"]],
                      on=["CHROM", "POS"], how="left")
merged.to_csv(OUT_CSV, index=False)

print(f"\nSaved: {OUT_CSV}  ({len(merged)} rows)")
print(merged[["CHROM", "POS", "GENE", "CONSEQUENCE", "IMPACT", "SIFT"]].head(10).to_string())
