"""an exploratory comparison of one numeric input feature."""
import numpy as np
import pandas as pd
from scipy.stats import ks_2samp


def compare_feature(reference, current, effect_threshold=0.15):
    if not 0 <= effect_threshold <= 1:
        raise ValueError('effect threshold must be between zero and one')
    reference = pd.to_numeric(pd.Series(reference), errors='raise')
    current = pd.to_numeric(pd.Series(current), errors='raise')
    a, b = reference.dropna().to_numpy(), current.dropna().to_numpy()
    if not len(a) or not len(b) or not np.isfinite(a).all() or not np.isfinite(b).all():
        raise ValueError('both windows need finite observed values')
    result = ks_2samp(a, b)
    return {
        'reference_observed': len(a), 'current_observed': len(b),
        'reference_missing_fraction': float(reference.isna().mean()),
        'current_missing_fraction': float(current.isna().mean()),
        'ks_statistic': float(result.statistic), 'pvalue': float(result.pvalue),
        'review_flag': bool(result.statistic > effect_threshold),
        'effect_threshold': effect_threshold,
    }
