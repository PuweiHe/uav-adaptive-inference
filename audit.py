"""Recompute archived validation peaks and report-derived arithmetic; no training."""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def summarize():
    runs = {}
    for name, classes in [('rtdetr', 5), ('yolo', 10)]:
        with (ROOT / 'evidence' / f'{name}_training.csv').open() as stream:
            rows = [{k.strip(): float(v) for k, v in row.items()} for row in csv.DictReader(stream)]
        runs[name] = {'classes_in_archived_confusion_matrix': classes, 'epochs': len(rows),
                      'peak_ap50': max(rows, key=lambda r: r['metrics/mAP50(B)']),
                      'peak_ap50_95': max(rows, key=lambda r: r['metrics/mAP50-95(B)']),
                      'last': rows[-1]}
    return {'validation_runs': runs, 'reported_test': {
        'source': 'Final_Report.pdf Table 4; not rerun',
        'small_ap50': .1395, 'large_ap50': .5660, 'hybrid_ap50': .5621,
        'map_retention_percent': 100*.5621/.5660,
        'runtime_saving_percent': 100*(1-2346.85/2867.25),
        'large_call_rate': .787,
        'constant_cost_estimate_seconds': 233.70+.787*2867.25,
        'reported_hybrid_seconds': 2346.85},
        'unresolved': ['Ten-class YOLO versus five-class final evaluation mapping absent',
                       'Final evaluation code, prediction files and split lists absent',
                       'Constant-cost estimate differs from reported hybrid timing',
                       'Checkpoint selection metadata not verified']}

if __name__ == '__main__':
    result = summarize()
    target = ROOT / 'evidence' / 'audit.json'
    target.write_text(json.dumps(result, indent=2) + '\n')
    print(target)
