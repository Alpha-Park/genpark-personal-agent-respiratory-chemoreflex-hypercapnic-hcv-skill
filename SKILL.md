---
name: genpark-personal-agent-respiratory-chemoreflex-hypercapnic-hcv-skill
version: 1.0.0
description: Zero-dependency sovereign personal agent skill for evaluating Hypercapnic Ventilatory Response (HCVR slope), central respiratory chemosensitivity, and breathing loop gain.
author: AlphaPark Inc.
license: Apache-2.0
tags:
  - personal-agent
  - ai-agent
  - openclaw
  - genpark
  - mcp
  - mcp-server
  - model-context-protocol
  - python
  - zero-dependency
  - wellness
  - productivity
  - production-ready
metadata:
  openclaw_compatible: true
  hermes_compatible: true
  zero_dependency: true
---

# Hypercapnic Ventilatory Response (HCVR) Skill

A sovereign personal agent capability for assessing central respiratory chemoreceptor sensitivity, hypercapnic ventilatory drive (dVE/dPETCO2), and respiratory loop gain stability.

## Core Capabilities
- **HCVR Slope Extraction**: Quantifies increase in minute ventilation per mmHg increase in end-tidal CO2.
- **Central Chemoreflex Stability**: Identifies controller loop gain anomalies linked to hyperventilation or periodic breathing.
- **CO2 Tolerance Profiling**: Stratifies adaptation levels for breathwork, athletic pacing, and altitude conditioning.
- **Respiratory Pacing Guidance**: Actionable protocols including resonant frequency and slow nasal pacing.

## Fast Invocation
```python
from client import RespiratoryChemoreflexClient

client = RespiratoryChemoreflexClient()
res = client.evaluate_hypercapnic_response(
    delta_petco2_mmhg=11.0,
    delta_minute_ventilation_l_min=25.3
)
print("HCVR Slope:", res["hcvr_slope_l_min_mmhg"], "L/min/mmHg")
print("Stability Score:", res["chemoreflex_stability_score"])
```
