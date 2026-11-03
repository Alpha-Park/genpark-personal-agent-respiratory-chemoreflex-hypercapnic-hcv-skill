"""
Hypercapnic Ventilatory Response (HCVR) & Central Chemoreflex Engine.
Provides deterministic, zero-dependency modeling of hypercapnic ventilatory response slope (S = dVE/dPETCO2),
ventilatory recruitment threshold (VRT), and central pontomedullary chemosensitivity loop gain.
"""

from typing import Dict, Any, List, Optional


class RespiratoryChemoreflexClient:
    """
    Deterministic client for calculating Hypercapnic Ventilatory Response (HCVR).
    Assesses central respiratory chemoreceptor gain, CO2 tolerance, and ventilatory stability
    during hypercapnic rebreathing or athletic hypoxia/hypercapnia conditioning.
    """

    def __init__(self):
        pass

    def evaluate_hypercapnic_response(
        self,
        delta_petco2_mmhg: float,
        delta_minute_ventilation_l_min: float,
        ventilatory_recruitment_threshold_mmhg: Optional[float] = None,
        baseline_petco2_mmhg: float = 38.0
    ) -> Dict[str, Any]:
        """
        Calculates HCVR slope S = delta_VE / delta_PETCO2 (in L/min/mmHg).
        Normative adult range: 1.5 to 3.5 L/min/mmHg.
        """
        if delta_petco2_mmhg <= 0 or delta_minute_ventilation_l_min <= 0:
            return {"error": "Delta PETCO2 and delta ventilation must be greater than zero"}

        hcvr_slope = round(delta_minute_ventilation_l_min / delta_petco2_mmhg, 2)

        # Chemoreflex Stability & Pacing Score (0 - 100):
        # Slope 1.8 - 3.2 -> 85 - 100.
        # Slope > 4.8 -> < 50 (Hypersensitive loop gain / panic hyperventilation).
        # Slope < 1.0 -> < 50 (Severe blunting / sleep apnea hypoventilation risk).
        if 1.8 <= hcvr_slope <= 3.2:
            score = 90.0 + min(10.0, (hcvr_slope - 1.8) * 5.0)
        elif 1.2 <= hcvr_slope < 1.8:
            score = 75.0 + ((hcvr_slope - 1.2) / 0.6) * 15.0
        elif 3.2 < hcvr_slope <= 4.2:
            score = 75.0 + ((4.2 - hcvr_slope) / 1.0) * 15.0
        elif hcvr_slope < 1.2:
            score = max(10.0, 40.0 + (hcvr_slope / 1.2) * 35.0)
        else:
            score = max(10.0, 75.0 - (hcvr_slope - 4.2) * 20.0)

        stability_score = round(min(100.0, max(5.0, score)), 1)

        if 1.6 <= hcvr_slope <= 3.4:
            tier = "BALANCED_CENTRAL_CHEMOREFLEX"
            interp = f"Normal balanced hypercapnic response slope ({hcvr_slope} L/min/mmHg); optimal central chemoreceptor loop gain."
            guidance = "Physiological CO2 sensing is healthy and stable. Maintain standard aerobic and breathwork routines."
        elif 1.0 <= hcvr_slope < 1.6:
            tier = "HIGH_CO2_TOLERANCE_ADAPTATION"
            interp = f"Blunted slope ({hcvr_slope} L/min/mmHg); reflects elevated CO2 tolerance (common in trained freedivers, yogis, or endurance athletes)."
            guidance = "High hypercapnic tolerance. Excellent breath-hold capacity; ensure adequate ventilation during high-intensity intervals."
        elif hcvr_slope > 3.4:
            tier = "CHEMOREFLEX_HYPERSENSITIVITY_LOOP_GAIN"
            interp = f"Elevated slope ({hcvr_slope} L/min/mmHg); hyper-reactive central chemoreceptor sensitivity and high controller loop gain."
            guidance = "Predisposition to hyperventilation or periodic breathing under stress. Practice slow 4-7-8 or resonant frequency (5.5 bpm) breathing."
        else:
            tier = "BLUNTED_CHEMOSENSITIVITY_HYPOVENTILATION_RISK"
            interp = f"Severely suppressed hypercapnic ventilatory drive ({hcvr_slope} L/min/mmHg < 1.0); risk of nocturnal CO2 retention."
            guidance = "Depressed hypercapnic chemoreflex. Recommend formal nocturnal polysomnography and blood gas evaluation."

        return {
            "delta_petco2_mmhg": delta_petco2_mmhg,
            "delta_minute_ventilation_l_min": delta_minute_ventilation_l_min,
            "hcvr_slope_l_min_mmhg": hcvr_slope,
            "ventilatory_recruitment_threshold_mmhg": ventilatory_recruitment_threshold_mmhg,
            "baseline_petco2_mmhg": baseline_petco2_mmhg,
            "chemoreflex_stability_score": stability_score,
            "classification": tier,
            "physiological_interpretation": interp,
            "actionable_guidance": guidance
        }
