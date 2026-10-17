"""compare fixed synthetic model outputs on the same mature labelled rows."""
import numpy as np
from sklearn.metrics import brier_score_loss, roc_auc_score


def evaluate_models(predictions, labels, cutoff_day=7, horizon_days=3):
    required = {'request_id', 'prediction_day', 'incumbent_score', 'candidate_score'}
    if not required.issubset(predictions.columns):
        raise ValueError('missing prediction fields')
    if not {'request_id', 'target', 'available_day'}.issubset(labels.columns):
        raise ValueError('missing label fields')
    if predictions['request_id'].isna().any() or not predictions['request_id'].is_unique:
        raise ValueError('prediction ids must be present and unique')
    if labels['request_id'].isna().any() or not labels['request_id'].is_unique:
        raise ValueError('label ids must be present and unique')
    if horizon_days < 0:
        raise ValueError('label horizon must be non-negative')
    mature = predictions[predictions['prediction_day'] <= cutoff_day - horizon_days]
    available = labels[labels['available_day'] <= cutoff_day]
    joined = mature.merge(available, on='request_id', how='left', validate='one_to_one')
    observed = joined.dropna(subset=['target'])
    coverage = len(observed) / len(mature) if len(mature) else 0.0
    report = {'mature_predictions': len(mature), 'labelled_predictions': len(observed),
              'label_coverage': coverage, 'status': 'collect_more_labels'}
    if not observed['target'].isin([0, 1]).all():
        raise ValueError('expected binary outcomes')
    if len(observed) < 30 or coverage < 0.9 or observed['target'].nunique() < 2:
        return report
    y = observed['target'].to_numpy()
    for name in ['incumbent', 'candidate']:
        scores = observed[name + '_score'].to_numpy(dtype=float)
        if not np.isfinite(scores).all() or ((scores < 0) | (scores > 1)).any():
            raise ValueError('invalid probabilities')
        report[name] = {'roc_auc': float(roc_auc_score(y, scores)),
                        'brier': float(brier_score_loss(y, scores))}
    better = (report['candidate']['brier'] < report['incumbent']['brier']
              and report['candidate']['roc_auc'] >= report['incumbent']['roc_auc'])
    report['status'] = 'review_candidate' if better else 'hold_candidate'
    return report
