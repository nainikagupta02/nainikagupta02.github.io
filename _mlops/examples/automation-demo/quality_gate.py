"""an illustrative validation gate for the synthetic learning exercise."""
import math


def check_candidate(report, min_auc=0.75):
    score = float(report['selected_validation_auc'])
    baseline = float(report['baseline_validation_auc'])
    if not all(math.isfinite(value) and 0 <= value <= 1 for value in [score, baseline]):
        raise ValueError('invalid validation metrics')
    if score < min_auc or score <= baseline:
        raise ValueError('candidate does not meet the toy validation gate')
    return score
