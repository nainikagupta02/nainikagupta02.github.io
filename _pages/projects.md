---
permalink: /projects/
title: "Projects"
author_profile: true
hide_title: true
---

## scPerturbEval

**Single-cell perturbation prediction evaluation**  
The University of Chicago  
Dr. Aly Khan

Built scPerturbEval, a modular Python CLI for evaluating single-cell perturbation prediction models with more than 15 metrics, including pathway enrichment metrics, across raw, PCA, and differentially expressed gene (DEG) spaces.

Benchmarked a distributional flow-matching model (scDFM) under the Norman additive split using four-fold cross-validation. It matched, but did not outperform, a simple additive baseline on differential-expression and pathway recovery.

**Tools:** Python, CLI, Single-cell analysis, PCA, Pathway enrichment, Cross-validation

## Medicare Claims Risk Stratification

**High-cost prediction and care-management targeting**  
Independent project

Built a SQL/DuckDB and Python pipeline using CMS DE-SynPUF synthetic Medicare claims for a cohort of 52,375 members. Engineered 27 utilization, spending, and chronic-condition features, with a training-only frozen high-cost threshold to prevent label leakage.

Compared logistic regression, XGBoost, and LightGBM for next-year high-cost prediction, achieving AUROC 0.72. Used SHAP for model interpretation; targeting the top 1% captured 2.0× more spending than a prior-year heuristic. Exported risk scores as FHIR R4 resources.

**Tools:** Python, SQL, DuckDB, XGBoost, LightGBM, SHAP, FHIR R4

## AML Genomics

**Mutation prediction and targeted variant detection**  
Independent project

Developed patient-grouped elastic-net models to predict FLT3-ITD and NPM1 mutations from BEAT-AML RNA-seq data. Externally validated frozen models on 151 TCGA-LAML patients without refitting, achieving AUROCs of 0.873 and 0.964, respectively.

Built a Nextflow pipeline using samtools, getITD, kallisto, and Pizzly. Recovered a 30-bp FLT3-ITD and the RUNX1–RUNX1T1 and PML–RARA fusions, with a preregistered negative control.

**Tools:** Nextflow, RNA-seq, Elastic net, samtools, getITD, kallisto, Pizzly

## Air Pollution & Type 2 Diabetes

**PM2.5 components and incident type 2 diabetes**  
The University of Chicago  
Dr. Briseis Aschebrook-Kilfoy

Curated SNOMED CT- and ICD-10-CM-coded electronic health records for 211,618 All of Us participants using SQL in BigQuery. Conducted exploratory analysis and used MICE for multiple imputation in R.

Modeled associations between ZIP3-linked PM2.5 constituents and incident type 2 diabetes using stratified Cox regression and quantile g-computation. Sulfate and sea salt were associated with higher risk, with sulfate contributing most strongly to the positive mixture association.

**Tools:** R, SQL, BigQuery, MICE, Survival analysis, Quantile g-computation  
**Status:** Manuscript in preparation

## Multi-Scale Mechanistic Modeling of Microalgal Photosynthesis

Plaksha University  
Dr. Saikat Chakraborty

Developed a mechanistic mathematical model of *Chlorella sorokiniana* photosynthesis across micro, meso, and macro scales in MATLAB. Modeled pigment-trap light-capture kinetics, thylakoid H⁺ transport, and CO₂-, nitrogen-, and light-dependent lipid, starch, and protein production.

Built ODE models for reaction kinetics and reaction–diffusion PDEs for proton transport. Reduced the PDEs to ODEs using central finite-difference discretization (method of lines) and solved the models in MATLAB using ode45 and pdepe.

**Tools:** MATLAB, ODEs, Reaction–diffusion PDEs, Method of lines, ode45, pdepe

## Library Recommendation System

Plaksha University  
Dr. Siddharth S

Built a hybrid recommendation system combining content-based and collaborative filtering methods in Python using more than 7,000 library transactions. Implemented the machine-learning pipeline, including data scraping, preprocessing, feature extraction, and model evaluation.

Reduced prediction error by 28% (RMSE = 0.45) by optimizing matrix factorization (SVD) and k-nearest neighbors (KNN) models.

**Tools:** Python, Recommendation systems, Collaborative filtering, SVD, KNN
