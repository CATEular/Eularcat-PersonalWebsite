---
title: Zotero Reading Notes
description: Turn one paper’s Zotero annotations into Obsidian notes that follow your reading habits
---

## Start with what you have read

Provide a paper title, short name or Zotero link. The agent reads the paper and its highlights, comments, area selections and drawings, then organizes them into readable topic notes. Links return you to the original PDF location, while quotations, your comments and AI explanations remain distinguishable.

Use it after reading a paper. Later runs add new or changed material and preserve manual edits. Related knowledge cards are optional.

## Install and set your preferences

Download the ZIP and place the extracted `zotero-reading-notes` folder in a skill directory supported by your agent. You need an accessible Zotero library and an Obsidian vault. The bundled offline evidence reader uses only the Python standard library.

On first use, ask the agent to configure your habits:

> Use $zotero-reading-notes. First confirm my Obsidian vault and paper-note folder, annotation color meanings, note language and level of detail, and whether to create knowledge cards. Save my preferences locally, then organize the paper I specify.

Copy `config.example.json` to `config.local.json` and let the agent fill it in from your answers. Existing preferences are reused; instructions in the current conversation take priority.

## Your colors, your meanings

Red may mean a question to one reader and an important conclusion to another. The skill asks first and also supports notes without color categories. Unconfigured colors remain source information; the agent organizes content from comments and the paper.

This is one optional example, requiring your confirmation:

| Color | Example meaning |
| --- | --- |
| Red | Open question |
| Green | Proposed approach |
| Yellow | Important knowledge |
| Blue | Definition |

Swap meanings, add colors or describe your own system. A proposed approach does not automatically resolve a question; context and applicable conditions still matter.

## Everyday use

> Organize all current annotations for “Paper title” in Obsidian. Use my saved preferences, update the existing note, and preserve my manual content and open questions.

Notes use meaningful topics and selected links to Zotero. Explanations without enough evidence stay marked for verification. Area selections and drawings need page inspection. The default scope is the paper you specify; detailed notes and knowledge cards can be enabled in your preferences.

## Files and local data

The package contains skill instructions, a preference example, setup guidance, local reading guidance and a read-only evidence extraction script. Keep personal settings, PDFs and annotation evidence in your own environment. Preserve `config.local.json` during upgrades and exclude it when sharing.

If a connector misses annotations, the agent can follow the bundled snapshot instructions. The script does not write to the Zotero database. Ambiguous papers need confirmation; without a confirmed destination, the agent drafts notes in the conversation first.
