"""
Example Usage: Hypercapnic Ventilatory Response (HCVR) Evaluation.
Demonstrates non-invasive calculation of central chemoreflex slope and CO2 tolerance.
"""

from client import RespiratoryChemoreflexClient


def main():
    client = RespiratoryChemoreflexClient()
    print("=== Hypercapnic Ventilatory Response (HCVR) Demo ===")

    # Test Case 1: Healthy normal adult chemoreflex
    res1 = client.evaluate_hypercapnic_response(
        delta_petco2_mmhg=11.0,
        delta_minute_ventilation_l_min=25.3,
        ventilatory_recruitment_threshold_mmhg=41.5,
        baseline_petco2_mmhg=38.0
    )
    print("\nTest Case 1: Healthy Normal Chemoreflex")
    print(f"  Delta PETCO2: {res1['delta_petco2_mmhg']} mmHg | Delta VE: {res1['delta_minute_ventilation_l_min']} L/min")
    print(f"  HCVR Slope: {res1['hcvr_slope_l_min_mmhg']} L/min/mmHg")
    print(f"  Stability Score: {res1['chemoreflex_stability_score']} / 100")
    print(f"  Classification: {res1['classification']}")
    print(f"  Guidance: {res1['actionable_guidance']}")

    # Test Case 2: High CO2 tolerance / breath-hold athlete
    res2 = client.evaluate_hypercapnic_response(
        delta_petco2_mmhg=14.0,
        delta_minute_ventilation_l_min=18.2
    )
    print("\nTest Case 2: High CO2 Tolerance Adaptation")
    print(f"  HCVR Slope: {res2['hcvr_slope_l_min_mmhg']} L/min/mmHg")
    print(f"  Stability Score: {res2['chemoreflex_stability_score']} / 100")
    print(f"  Classification: {res2['classification']}")
    print(f"  Guidance: {res2['actionable_guidance']}")

    # Test Case 3: Chemoreflex hypersensitivity / panic hyperventilation pattern
    res3 = client.evaluate_hypercapnic_response(
        delta_petco2_mmhg=8.0,
        delta_minute_ventilation_l_min=36.0
    )
    print("\nTest Case 3: Chemoreflex Hypersensitivity")
    print(f"  HCVR Slope: {res3['hcvr_slope_l_min_mmhg']} L/min/mmHg")
    print(f"  Stability Score: {res3['chemoreflex_stability_score']} / 100")
    print(f"  Classification: {res3['classification']}")
    print(f"  Guidance: {res3['actionable_guidance']}")


if __name__ == "__main__":
    main()
