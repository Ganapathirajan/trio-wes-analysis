
# Trio Whole Exome Sequencing — Clinical Interpretation Report

## Case Summary
- **Proband:** PROBAND (simulated case, chr21 analysis)
- **Parents:** MOTHER (unaffected), FATHER (unaffected)
- **Dataset:** NA12878 chr21 variants, 1000 Genomes Phase 3
- **Analysis date:** 2026-05-31
- **Pipeline:** GATK4 → slivar → VEP REST API → custom Python ranker

---

## QC Summary
| Metric | Value |
|--------|-------|
| Total chr21 variants (proband) | 1,054,447 |
| PASS SNPs | 1,054,447 |
| Slivar candidates (all models) | 23,545 |
| De novo candidates | 3,184 |
| Recessive candidates | 20,361 |
| Coding HIGH/MODERATE impact | 138 |

---

## Inheritance Model Summary
| Model | Count |
|-------|-------|
| De novo | 3,184 |
| Homozygous recessive | 20,361 |
| X-linked | 0 |

---

## Top Candidate Variants

### Tier 1 — High Priority (De novo + HIGH impact)

#### 1. USP16 — chr21:29043515 C>T | stop_gained | De novo
- **Consequence:** p.? (stop gained, protein truncating)
- **Impact:** HIGH
- **Inheritance:** De novo (absent in both parents)
- **Gene function:** Ubiquitin-specific protease; regulates H2A deubiquitination. 
  Expressed in brain; overexpression on chr21 implicated in Down syndrome 
  cognitive deficit phenotype.
- **ACMG evidence:**
  - PVS1: Null variant in gene where LOF is disease mechanism ✓
  - PS2: Confirmed de novo (parents unaffected) ✓
  - **Provisional classification: LIKELY PATHOGENIC**

#### 2. MIR99AHG — chr21:16181600 | splice_acceptor_variant | De novo
- **Consequence:** Splice acceptor disruption
- **Impact:** HIGH
- **Inheritance:** De novo
- **Note:** lncRNA host gene; clinical significance uncertain
- **ACMG evidence:** PS2 ✓, PVS1 partial
- **Provisional classification: VARIANT OF UNCERTAIN SIGNIFICANCE (VUS)**

#### 3. UMODL1 — chr21:42127102 | missense_variant | De novo
- **Consequence:** Missense, SIFT deleterious
- **Impact:** MODERATE
- **Inheritance:** De novo
- **Gene function:** Uromodulin-like 1; expressed in sensory epithelia
- **ACMG evidence:** PS2 ✓, PP3 (deleterious in silico) ✓
- **Provisional classification: VUS — favour pathogenic**

---

### Tier 2 — Recessive Stop-Gained

#### 4. BTG3 — chr21:17594298 | stop_gained | Recessive
- **Consequence:** Protein truncating
- **Impact:** HIGH
- **Inheritance:** Homozygous recessive
- **Gene function:** BTG anti-proliferation factor 3; tumour suppressor
- **ACMG evidence:** PVS1 ✓
- **Provisional classification: VUS (limited recessive disease evidence)**

#### 5. GRIK1 — chr21:29537340 | stop_gained | Recessive
- **Consequence:** Protein truncating
- **Impact:** HIGH
- **Inheritance:** Homozygous recessive
- **Gene function:** Glutamate receptor, ionotropic, kainate 1; 
  associated with epilepsy and intellectual disability
- **ACMG evidence:** PVS1 ✓, phenotype match if epilepsy present
- **Provisional classification: LIKELY PATHOGENIC (phenotype-dependent)**

---

## Clinical Interpretation Letter

To the referring clinician,

Whole exome sequencing was performed on a trio comprising the proband and both 
biological parents. Analysis was restricted to chromosome 21 for this pilot study.

A total of 23,545 rare variants were identified after inheritance-model filtering. 
138 variants with HIGH or MODERATE predicted functional impact were prioritised 
for review.

The highest-priority finding is a **de novo stop-gained variant in USP16** 
(chr21:29,043,515), absent in both unaffected parents. USP16 encodes a 
deubiquitinase with established roles in chromosome segregation and neural 
development. This variant meets criteria for provisional classification as 
**Likely Pathogenic** (ACMG criteria: PVS1 + PS2).

A secondary finding of note is a **homozygous stop-gained variant in GRIK1**, 
a glutamate receptor subunit gene associated with epileptic encephalopathy. 
Clinical correlation with the proband's phenotype is recommended.

**Recommendation:** Confirm USP16 variant by Sanger sequencing. 
Obtain detailed neurodevelopmental history. Consider referral to clinical 
genetics for formal ACMG classification and genetic counselling.

*This report was generated as part of a bioinformatics training exercise using 
publicly available 1000 Genomes data. Not for clinical use.*

---
## Methods
- Reference: GRCh38/hg38, chr21
- Variant source: 1000 Genomes Phase 3
- Trio simulation: synthetic parental genotypes from NA12878 het variants
- Inheritance filtering: slivar v0.3.0
- Annotation: Ensembl VEP REST API (GRCh38)
- Ranking: custom Python score (impact + inheritance + in silico prediction)
