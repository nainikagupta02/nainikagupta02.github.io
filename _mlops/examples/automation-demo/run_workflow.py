"""a local sequential runner; no model is deployed by this script."""
import argparse
import json
from pathlib import Path
import re
import subprocess
import sys
from quality_gate import check_candidate


def run_workflow(run_id):
    if not re.fullmatch(r'[a-z0-9][a-z0-9_-]{0,63}', run_id):
        raise ValueError('use a short lowercase run id with letters, numbers, _ or -')
    output = Path('artifacts') / run_id
    manifest = Path('workflow-runs') / f'{run_id}.json'
    if output.exists() or manifest.exists():
        raise FileExistsError('run id already exists; inspect it and choose a new id')
    manifest.parent.mkdir(parents=True, exist_ok=True)
    state = {'run_id': run_id, 'status': 'running', 'stage': 'train'}

    def record():
        manifest.write_text(json.dumps(state, indent=2) + '\n')

    record()
    try:
        trainer = Path(__file__).with_name('lifecycle_demo.py').resolve()
        subprocess.run([sys.executable, str(trainer), '--output', str(output)], check=True)
        state['stage'] = 'validate'
        record()
        report = json.loads((output / 'run.json').read_text())
        score = check_candidate(report)
        state.update(status='candidate', stage='complete', validation_auc=score,
                     model_path=str(output / 'pipeline.joblib'))
    except Exception as error:
        state.update(status='failed', error=str(error))
        record()
        raise
    record()
    return state


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run-id', required=True)
    print(json.dumps(run_workflow(parser.parse_args().run_id), indent=2))
