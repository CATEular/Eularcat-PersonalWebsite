---
title: Analog IC Notes
description: From papers to your own analog IC notes
---

## What it does

Organizes publication details, architectures, key circuits, measurements and citations into Markdown / Obsidian notes, preserving figures and LaTeX equations

Adapted from DC-DC Buck Reader, with a Buck reading template and a general template for analog and mixed-signal IC papers

## Get started

Download and extract the package, then place `analog-ic-notes` in the skill directory supported by your tool

Invoke `$analog-ic-notes` in a new conversation and provide the paper or PDF, note language and output location

> Use Analog IC Notes to read this paper and create Markdown notes with circuit analysis, test conditions, citations and figures

## Your own paths

Copy `config.example.json` to a local `config.local.json` and adjust the directories

```json
{
  "paths": {
    "papers": "./papers",
    "notes": "./notes",
    "images": "./notes/assets"
  },
  "language": "en"
}
```

Relative paths resolve from the configuration file, absolute paths are also supported, keep personal configuration outside shared packages

The figure helpers require Python and the listed dependencies

```sh
python -m pip install -r requirements.txt
python scripts/paths.py --config config.local.json
python scripts/extract_figures.py paper.pdf --config config.local.json --paper-id my-paper
```

## Keep the evidence

Mark missing information, distinguish measurements from simulations and your own deductions, and check conditions before comparing papers

The skill does not run circuit simulations or validate a design, notes should be checked against the original paper

## In the package

- General analog IC and Buck paper templates
- Configurable paper, note and image directories
- Helpers for PDF image regions and vector figure crops
- Checks for metrics, citations and figures
