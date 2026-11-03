"""
MCP Server for Hypercapnic Ventilatory Response (HCVR) Skill.
Exposes JSON-RPC Model Context Protocol tools for assessing central respiratory chemoreflex sensitivity and CO2 tolerance.
"""

import sys
import json
from typing import Dict, Any
from client import RespiratoryChemoreflexClient


def get_tools_manifest() -> Dict[str, Any]:
    return {
        "tools": [
            {
                "name": "evaluate_hypercapnic_response",
                "description": "Calculates Hypercapnic Ventilatory Response (HCVR slope in L/min/mmHg), chemoreflex stability score, and breathing control guidance.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "delta_petco2_mmhg": {
                            "type": "number",
                            "description": "Increase in end-tidal CO2 during rebreathing in mmHg (e.g. 10.0 mmHg)."
                        },
                        "delta_minute_ventilation_l_min": {
                            "type": "number",
                            "description": "Increase in minute ventilation in L/min (e.g. 24.0 L/min)."
                        },
                        "ventilatory_recruitment_threshold_mmhg": {
                            "type": "number",
                            "description": "Optional PETCO2 threshold where hyperpnea begins in mmHg."
                        },
                        "baseline_petco2_mmhg": {
                            "type": "number",
                            "description": "Resting baseline PETCO2 in mmHg (typically 36 - 42 mmHg).",
                            "default": 38.0
                        }
                    },
                    "required": ["delta_petco2_mmhg", "delta_minute_ventilation_l_min"]
                }
            }
        ]
    }


def handle_request(client: RespiratoryChemoreflexClient, req: Dict[str, Any]) -> Dict[str, Any]:
    method = req.get("method")
    params = req.get("params", {})
    req_id = req.get("id")

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": get_tools_manifest()
        }
    elif method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {})

        if name == "evaluate_hypercapnic_response":
            vrt = args.get("ventilatory_recruitment_threshold_mmhg")
            if vrt is not None:
                vrt = float(vrt)

            res = client.evaluate_hypercapnic_response(
                delta_petco2_mmhg=float(args.get("delta_petco2_mmhg", 10.0)),
                delta_minute_ventilation_l_min=float(args.get("delta_minute_ventilation_l_min", 24.0)),
                ventilatory_recruitment_threshold_mmhg=vrt,
                baseline_petco2_mmhg=float(args.get("baseline_petco2_mmhg", 38.0))
            )
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(res, indent=2)
                        }
                    ]
                }
            }
        else:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {
                    "code": -32601,
                    "message": f"Method {name} not found"
                }
            }
    else:
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {
                "code": -32600,
                "message": "Invalid request"
            }
        }


def main():
    client = RespiratoryChemoreflexClient()
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle_request(client, req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err_resp = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": str(e)}
            }
            sys.stdout.write(json.dumps(err_resp) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
