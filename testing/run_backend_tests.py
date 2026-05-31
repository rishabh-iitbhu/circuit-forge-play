import os
import json
from datetime import datetime
import pandas as pd

from lib.calculations import CircuitCalculator, BuckInputs, PFCInputs, validate_inputs
from lib.component_suggestions import suggest_mosfets


TESTING_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'testing')
os.makedirs(TESTING_DIR, exist_ok=True)


def run_tests():
    calc = CircuitCalculator()

    scenarios = []

    # Normal buck scenario
    scenarios.append({
        'id': 'buck_normal',
        'type': 'buck',
        'desc': 'Standard 12V->5V, moderate power',
        'inputs': {
            'v_in_min': 11.0,
            'v_in_max': 13.2,
            'v_out_min': 4.9,
            'v_out_max': 5.1,
            'p_out_max': 20.0,
            'efficiency': 0.92,
            'switching_freq': 300000.0,
            'v_ripple_max': 0.05,
            'v_in_ripple': 0.3,
            'i_out_ripple': 0.5,
            'v_overshoot': 0.1,
            'v_undershoot': 0.1,
            'i_loadstep': 2.0
        }
    })

    # Edge high-frequency scenario
    scenarios.append({
        'id': 'buck_hf',
        'type': 'buck',
        'desc': 'High switching frequency scenario',
        'inputs': {
            'v_in_min': 20.0,
            'v_in_max': 24.0,
            'v_out_min': 3.2,
            'v_out_max': 3.3,
            'p_out_max': 10.0,
            'efficiency': 0.90,
            'switching_freq': 1000000.0,
            'v_ripple_max': 0.01,
            'v_in_ripple': 0.2,
            'i_out_ripple': 0.2,
            'v_overshoot': 0.05,
            'v_undershoot': 0.05,
            'i_loadstep': 1.0
        }
    })

    # Low-voltage, high-current scenario that may fail availability
    scenarios.append({
        'id': 'buck_high_current',
        'type': 'buck',
        'desc': 'Low Vout, high power -> high current requirement',
        'inputs': {
            'v_in_min': 12.0,
            'v_in_max': 14.0,
            'v_out_min': 1.2,
            'v_out_max': 1.8,
            'p_out_max': 30.0,
            'efficiency': 0.85,
            'switching_freq': 200000.0,
            'v_ripple_max': 0.02,
            'v_in_ripple': 0.5,
            'i_out_ripple': 2.0,
            'v_overshoot': 0.1,
            'v_undershoot': 0.1,
            'i_loadstep': 5.0
        }
    })

    # PFC normal scenario
    scenarios.append({
        'id': 'pfc_normal',
        'type': 'pfc',
        'desc': 'Standard PFC case',
        'inputs': {
            'v_in_min': 90.0,
            'v_in_max': 132.0,
            'v_out_min': 400.0,
            'v_out_max': 410.0,
            'p_out_max': 100.0,
            'efficiency': 0.95,
            'switching_freq': 100000.0,
            'line_freq_min': 50.0,
            'v_ripple_max': 1.0
        }
    })

    # Invalid input scenario to validate validation handling
    scenarios.append({
        'id': 'invalid_inputs',
        'type': 'buck',
        'desc': 'Negative values should be rejected',
        'inputs': {
            'v_in_min': -5.0,
            'v_in_max': 0.0,
            'v_out_min': 0.0,
            'v_out_max': 0.0,
            'p_out_max': -10.0,
            'efficiency': 0.0,
            'switching_freq': -100.0,
            'v_ripple_max': 0.0,
            'v_in_ripple': 0.0,
            'i_out_ripple': 0.0,
            'v_overshoot': 0.0,
            'v_undershoot': 0.0,
            'i_loadstep': 0.0
        }
    })

    records = []

    for s in scenarios:
        rec = {'test_id': s['id'], 'description': s['desc'], 'type': s['type']}
        inputs = s['inputs']

        # Validation
        is_valid = validate_inputs(inputs)
        rec['valid_inputs'] = is_valid

        if not is_valid:
            rec['result'] = 'invalid_inputs'
            records.append(rec)
            continue

        if s['type'] == 'buck':
            buck_inputs = BuckInputs(**inputs)
            results = calc.calculate_buck(buck_inputs)

            # Collect numeric outputs
            rec.update({
                'inductance_uH': results.inductance * 1e6,
                'output_cap_uF': results.output_capacitance * 1e6,
                'input_cap_uF': results.input_capacitance * 1e6,
                'duty_cycle': results.duty_cycle_max,
            })

            # Run MOSFET suggestion to verify rationale text presence
            mosfets = suggest_mosfets(
                max_voltage=inputs['v_in_max'],
                max_current=inputs['p_out_max'] / inputs['v_out_min'],
                frequency_hz=inputs['switching_freq'],
                use_web_search=False
            )

            rec['mosfet_suggestions'] = len(mosfets)
            if mosfets:
                # sample first reason
                rec['mosfet_sample_reason'] = mosfets[0].reason
                # checks for required phrases
                rec['reason_has_IDmax'] = 'IDmax' in mosfets[0].reason or 'ID=' in mosfets[0].reason
                rec['reason_has_rdson_temp'] = 'RDS(on)' in mosfets[0].reason or 'RDS(on) used' in mosfets[0].reason
            else:
                rec['mosfet_sample_reason'] = ''
                rec['reason_has_IDmax'] = False
                rec['reason_has_rdson_temp'] = False

        elif s['type'] == 'pfc':
            pfc_inputs = PFCInputs(**inputs)
            results = calc.calculate_pfc(pfc_inputs)

            rec.update({
                'inductance_H': results.inductance,
                'capacitance_F': results.capacitance,
                'ripple_current_A': results.ripple_current,
            })

        records.append(rec)

    # Create DataFrame and write to Excel
    df = pd.DataFrame(records)
    timestamp = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    out_path = os.path.join(TESTING_DIR, f'backend_test_results_{timestamp}.xlsx')
    df.to_excel(out_path, index=False)

    # Also write a JSON summary
    json_path = os.path.join(TESTING_DIR, f'backend_test_results_{timestamp}.json')
    with open(json_path, 'w', encoding='utf-8') as fh:
        json.dump(records, fh, indent=2)

    print(f"Test run complete. Excel: {out_path}")
    return out_path, json_path


if __name__ == '__main__':
    run_tests()
