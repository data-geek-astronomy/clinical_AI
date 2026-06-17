---
title: Surge Pricing Impact Analysis
emoji: 🚗
colorFrom: red
colorTo: blue
sdk: gradio
sdk_version: 4.0.0
app_file: app.py
pinned: false
---

# Surge Pricing Impact Analysis

**How does surge pricing actually affect riders and drivers?**

This tool simulates ride-sharing marketplace dynamics and uses causal inference to isolate the true impact of surge pricing.

## What It Does

- Simulates realistic marketplace data with confounders
- Applies 3 causal inference methods: PSM, Synthetic Control, ITS
- Interactive visualization of surge pricing effects

## Methods

- **Propensity Score Matching:** Match surge/no-surge scenarios
- **Synthetic Control:** Build counterfactual from control periods  
- **Interrupted Time Series:** Detect structural breaks

## GitHub

https://github.com/data-geek-astronomy/surge_pricing_analysis
