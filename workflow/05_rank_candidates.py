#!/usr/bin/env python3
"""
05_rank_candidates.py
Score and rank annotated candidates.

Scoring rubric:
  +40  IMPACT == HIGH
  +20  IMPACT == MODERATE
  +20  stop_gained / stop_lost
  +15  splice_acceptor / splice_donor
  +10  missense_variant
  +15  SIFT == deleterious (exact)
  + 5  SIFT contains deleterious (low_confidence etc.)
  +30  De novo inheritance (highest clinical weight)
  +10  Recessive inheritance

Input:  results/annotated/coding_candidates.csv
Output: results/annotated/candidates_ranked.csv

Usage:
    python workflow/05_rank_candidates.py
"""

import os
import pandas as pd

IN_CSV  = "results/annotated/coding_candidates.csv"
OUT_CSV = "results/annotated/candidates_ranked.csv"

os.makedirs("results/annotated", exist_ok=True)

df = pd.read_csv(IN_CSV)
df["CHROM"] = df["CHROM"].astype(str)


def score(row) -> int:
    s = 0
    # Impact
    if row["IMPACT"] == "HIGH":     s += 40
    if row["IMPACT"] == "MODERATE": s += 20
    # Consequence
    csq = str(row["CONSEQUENCE"])
    if "stop"   in csq: s += 20
    if "splice" in csq: s += 15
    if "missense" in csq: s += 10
    # In silico
    sift = str(row["SIFT"])
    if sift == "deleterious":          s += 15
    elif "deleterious" in sift:        s += 5
    # Inheritance model
    if str(row.get("DENOVO",  ".")) not in (".", "nan"): s += 30
    if str(row.get("RECESSIVE", ".")) not in (".", "nan"): s += 10
    return s


df["RANK_SCORE"] = df.apply(score, axis=1)
df = df.sort_values("RANK_SCORE", ascending=False).reset_index(drop=True)
df["RANK"] = df.index + 1

df.to_csv(OUT_CSV, index=False)

print("=== TOP 20 CANDIDATES ===")
cols = ["RANK", "CHROM", "POS", "GENE", "CONSEQUENCE", "IMPACT", "SIFT", "DENOVO", "RANK_SCORE"]
print(df[cols].head(20).to_string(index=False))
print(f"\nFull table saved: {OUT_CSV}  ({len(df)} variants)")
