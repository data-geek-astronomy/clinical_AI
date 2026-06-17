---
title: Surge Pricing Impact Analysis
emoji: 🚗
colorFrom: red
colorTo: blue
sdk: streamlit
sdk_version: 1.27.0
app_file: app.py
pinned: false
---

# Surge Pricing Impact Analysis

**How does surge pricing actually affect riders and drivers?**

This tool lets you explore the real impact of surge pricing by simulating a marketplace and then using causal inference methods to isolate what surge actually does—as opposed to just comparing good days to bad days.

## What It Does

I built a marketplace simulator that creates realistic demand/supply dynamics with the same confounding factors that exist in real data (weather, events, day-of-week effects). Then I apply causal inference to separate the actual effect of surge pricing from these confounders.

## Methods

- **Propensity Score Matching (PSM):** Match surge to no-surge days on confounders
- **Synthetic Control Method:** Build a synthetic "no surge" counterfactual
- **Interrupted Time Series (ITS):** Detect level & slope changes at intervention

## Why This Project

At ride-sharing companies, the hard part isn't collecting data—it's figuring out what actually caused what. Did completion rates go up because of surge pricing, or just because it was Friday night? This is the kind of problem causal inference solves.

## Live Demo

**GitHub:** https://github.com/data-geek-astronomy/surge_pricing_analysis

**Try it here:** Use the sliders on the left to adjust surge parameters and see real-time impact!
