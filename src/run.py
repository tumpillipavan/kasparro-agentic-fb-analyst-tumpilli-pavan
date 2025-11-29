
import sys, os, json, argparse, yaml
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.orchestrator.orchestrator import AgentOrchestrator

def load_config():
    with open('config/config.yaml', 'r') as f:
        return yaml.safe_load(f)

def save_outputs(results, outdir='reports'):
    os.makedirs(outdir, exist_ok=True)
    insights = results['steps'].get('insights', {})
    with open(os.path.join(outdir, 'insights.json'), 'w') as f:
        json.dump(insights, f, indent=2)
    creatives = results['steps'].get('creative_improvements', {})
    with open(os.path.join(outdir, 'creatives.json'), 'w') as f:
        json.dump(creatives, f, indent=2)
    with open(os.path.join(outdir, 'report.md'), 'w') as f:
        f.write(f"# Report for {results.get('execution_id')}\n\n")
        f.write(json.dumps(results['final_report'], indent=2))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('query', type=str, help='Analysis query')
    args = parser.parse_args()
    config = load_config()
    orchestrator = AgentOrchestrator(config)
    results = orchestrator.execute_analysis(args.query)
    save_outputs(results)
    print('Done. Reports in reports/')

if __name__ == '__main__':
    main()
