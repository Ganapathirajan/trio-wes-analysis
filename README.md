# Trio WES Analysis for Rare Disease Diagnosis.

![Pipeline](https://img.shields.io/badge/pipeline-slivar%20%7C%20GATK4%20%7C%20VEP-blue)
![Dataset](https://img.shields.io/badge/dataset-1000%20Genomes%20Phase%203-green)
![Status](https://img.shields.io/badge/status-complete-brightgreen)
![Platform](https://img.shields.io/badge/platform-Google%20Colab-orange)

## Overview

End-to-end trio whole exome sequencing (WES) analysis pipeline for rare disease diagnosis.  
Simulates a clinical diagnostic workup: inheritance filtering → variant annotation → candidate ranking → clinical report.

**Dataset:** NA12878 (chr21), 1000 Genomes Phase 3.  
**Scope:** Chromosome 21 (Colab-compatible subset).  
**Trio:** Synthetic proband + parents derived from real NA12878 heterozygous variants.

---

## Pipeline Summary

```
1000G chr21 VCF
      │
      ▼
Extract NA12878 (bcftools)
      │
      ▼
Simulate trio genotypes (Python)
      │
      ▼
Inheritance filtering — slivar v0.3.0
  ├── De novo:    3,184 variants
  ├── Recessive: 20,361 variants
  └── X-linked:       0 variants
      │
      ▼
VEP REST API annotation (Ensembl GRCh38)
      │
      ▼
Coding variant filter (HIGH / MODERATE impact)
  └── 138 candidates
      │
      ▼
Custom Python ranker
  └── Score = impact + inheritance model + SIFT + consequence
      │
      ▼
Clinical report (Markdown)
  └── Top hit: USP16 de novo stop_gained — Likely Pathogenic
```

---

## Key Findings

| Rank | Gene | Position | Consequence | Impact | Inheritance | ACMG |
|------|------|----------|-------------|--------|-------------|------|
| 1 | **USP16** | chr21:29,043,515 | stop_gained | HIGH | De novo | Likely Pathogenic |
| 2 | MIR99AHG | chr21:16,181,600 | splice_acceptor | HIGH | De novo | VUS |
| 3 | UMODL1 | chr21:42,127,102 | missense | MODERATE | De novo | VUS favour pathogenic |
| 4 | BTG3 | chr21:17,594,298 | stop_gained | HIGH | Recessive | VUS |
| 5 | **GRIK1** | chr21:29,537,340 | stop_gained | HIGH | Recessive | Likely Pathogenic* |

*phenotype-dependent

---

## Tools & Versions

| Tool | Version | Purpose |
|------|---------|---------|
| samtools | 1.13 | BAM/VCF handling |
| bcftools | 1.13 | VCF filtering & extraction |
| GATK | 4.4.0.0 | Joint genotyping framework |
| slivar | 0.3.0 | Inheritance model filtering |
| Ensembl VEP REST API | GRCh38 | Variant annotation |
| Python | 3.11 | Simulation, ranking, reporting |
| pandas | latest | Data manipulation |

---

## Repository Structure

```
04-trio-wes-analysis/
├── README.md                        # This file
├── environment.yml                  # Conda environment
├── .gitignore                       # Excludes large genomic files
│
├── data/
│   ├── download_reference.sh        # Download chr21 reference
│   ├── download_1000g_vcf.sh        # Download 1000G chr21 VCF
│   └── trio.ped                     # Pedigree file (PROBAND/MOTHER/FATHER)
│
├── workflow/
│   ├── 00_setup.sh                  # Tool installation
│   ├── 01_extract_sample.sh         # Extract NA12878 from 1000G VCF
│   ├── 02_simulate_trio.py          # Synthetic trio generation
│   ├── 03_slivar_inheritance.sh     # Inheritance filtering
│   ├── 04_vep_annotation.py         # VEP REST API batch annotation
│   └── 05_rank_candidates.py        # Variant scoring & ranking
│
├── results/
│   ├── qc/                          # QC metrics (flagstat etc.)
│   ├── slivar/                      # Inheritance-filtered VCF
│   └── annotated/
│       ├── candidates_ranked.csv    # Final ranked candidate table
│       ├── coding_candidates.csv    # HIGH/MODERATE impact variants
│       └── denovo_top50_annotated.csv
│
├── notebooks/
│   └── Project_04_Trio_WES_Analysis.ipynb   # Full Colab notebook
│
└── report/
    └── clinical_interpretation.md   # Clinical report (USP16 top hit)
```

---

## How to Reproduce

### Option A — Google Colab (recommended)
1. Open `notebooks/Project_04_Trio_WES_Analysis.ipynb` in Colab
2. Run all cells in order
3. Runtime: ~45 minutes

### Option B — Local
```bash
# Clone repo
git clone https://github.com/YOUR_USERNAME/04-trio-wes-analysis
cd 04-trio-wes-analysis

# Install environment
conda env create -f environment.yml
conda activate trio-wes

# Run pipeline
bash workflow/00_setup.sh
bash workflow/01_extract_sample.sh
python workflow/02_simulate_trio.py
bash workflow/03_slivar_inheritance.sh
python workflow/04_vep_annotation.py
python workflow/05_rank_candidates.py
```

---

## Data Sources

| Resource | URL |
|----------|-----|
| 1000 Genomes Phase 3 chr21 VCF | https://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/ |
| hg38 chr21 reference | https://hgdownload.soe.ucsc.edu/goldenPath/hg38/chromosomes/ |
| Ensembl VEP REST API | https://rest.ensembl.org/vep/human/region |
| slivar GitHub | https://github.com/brentp/slivar |

---

## Limitations & Notes

- Analysis restricted to **chr21 only** (Colab storage constraint)
- Parental genotypes are **synthetically simulated** — not real family data
- De novo calls at ~10% rate by design (random seed 42)
- VEP annotation via REST API (no local cache) — slower but zero-install
- HGVSp fields missing (VEP REST returns abbreviated output without `--hgvs` flag)
- This is a **training project** — not validated for clinical use

---

## Skills Demonstrated

- Trio joint genotyping concepts (GATK4)
- Inheritance model filtering (de novo, recessive, x-linked)
- Variant annotation via REST API (VEP/Ensembl)
- Custom variant prioritisation scoring
- ACMG classification framework (PVS1, PS2, PP3)
- Clinical report writing
- Reproducible bioinformatics pipeline design
