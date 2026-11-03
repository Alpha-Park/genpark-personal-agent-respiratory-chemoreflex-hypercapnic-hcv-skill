# Hypercapnic Ventilatory Response (HCVR) Skill

[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![Zero Dependencies](https://img.shields.io/badge/zero--dependencies-standard--lib-brightgreen.svg)](requirements.txt)
[![MCP Protocol Ready](https://img.shields.io/badge/mcp-protocol--ready-orange.svg)](mcp_server.py)
[![OpenClaw Certified](https://img.shields.io/badge/openclaw-certified-purple.svg)](SKILL.md)

Zero-dependency sovereign personal agent skill for non-invasive evaluation of Hypercapnic Ventilatory Response (HCVR slope), central respiratory chemosensitivity, and CO2 tolerance.

```mermaid
flowchart TD
    Capnometry["End-Tidal CO2 & Spirometry Sensors"] --> LinearReg["Linear Regression Slope (dVE / dPETCO2)"]
    LinearReg --> LoopGain["Chemoreflex Loop Gain & Threshold Analysis"]
    LoopGain --> PacingEngine["Respiratory Chemoreflex Stability Engine"]
    PacingEngine --> Agent["OpenClaw / Hermes Personal Agent Actions"]
```

## Features
- **Deterministic Math**: Pure Python standard library implementation with zero external dependencies.
- **Respiratory Physiology Standards**: Implements validated Read rebreathing linear sensitivity slope calculations.
- **Chemoreflex Loop Gain Stratification**: Quantitative evaluation of central controller sensitivity and periodic breathing vulnerability.
- **Model Context Protocol (MCP)**: Native JSON-RPC tool integration for LLMs and autonomous agents.

## Quickstart

```python
from client import RespiratoryChemoreflexClient

client = RespiratoryChemoreflexClient()
result = client.evaluate_hypercapnic_response(
    delta_petco2_mmhg=11.0,
    delta_minute_ventilation_l_min=25.3
)
print("HCVR Slope:", result["hcvr_slope_l_min_mmhg"])
print("Classification:", result["classification"])
```

## License
Apache-2.0
