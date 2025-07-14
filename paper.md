---
title: "Automated System for Scoring and Interpretation of the Satisfaction with Life Scale"
authors:
  - name: Ruben Baptista
    affiliation: "1"
affiliations:
  - name: NAEP – Núcleo de Apoio Emocional e Psicológico
    index: 1
date: 2025-07-08
bibliography: paper.bib
---

# Summary

This paper presents a Python-based automated system for scoring and interpreting the Satisfaction With Life Scale (SWLS). The tool includes a graphical user interface developed with Tkinter, automates score calculation, enforces response validation, and generates PDF reports summarizing results with clinical interpretation. Designed for psychological professionals and researchers, the system improves efficiency and reduces human error during assessment. Initial tests in simulated environments show promising accuracy and usability.

# Statement of need

Manual scoring of psychological scales such as SWLS can be time-consuming and prone to error. Although the SWLS is widely used, few tools offer automated, localized, and clinically valid reporting capabilities. This software provides a localized, validated, and user-friendly scoring tool that enhances standardization and usability in both clinical and research settings.

# Installation

This software requires Python 3.10+. To install:

```bash
git clone https://github.com/SEU-USUARIO/SWLS-AutoScore
cd SWLS-AutoScore
pip install -r requirements.txt
python main.py
