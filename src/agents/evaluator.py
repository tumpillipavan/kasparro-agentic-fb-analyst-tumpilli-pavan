from typing import List, Dict, Any

class EvaluatorAgent:
    def __init__(self, config=None):
        self.config = config or {}

    def validate_hypotheses(self, hypotheses: List[Dict[str,Any]], data_summary: Dict[str,Any]):
        results = []
        perf = data_summary.get('performance_metrics',{})
        avg_ctr = perf.get('avg_ctr') or 0
        avg_roas = perf.get('avg_roas') or 0
        for h in hypotheses:
            base = h.get('confidence_initial', 0.5)
            score = base
            metrics = h.get('metrics_to_validate', [])
            if any('ctr' in m for m in metrics):
                if avg_ctr and avg_ctr < 0.02:
                    score = min(1.0, score + 0.2)
            if any('roas' in m for m in metrics):
                if avg_roas and avg_roas < 1.5:
                    score = min(1.0, score + 0.2)
            status = 'validated' if score >= 0.6 else 'partially_validated'
            results.append({
                "hypothesis_id": h.get('hypothesis_id'),
                "status": status,
                "confidence_final": round(score, 2),
                "supporting_evidence": [f"avg_ctr={avg_ctr}", f"avg_roas={avg_roas}"],
                "recommendation": "Run A/B tests for creatives" if any('ctr' in m for m in metrics) else "Check landing page and conversion funnel"
            })
        overall = round(sum([r['confidence_final'] for r in results]) / len(results), 2) if results else 0.5
        return {"validated_hypotheses": results, "overall_confidence": overall}

    def calculate_quantitative_confidence(self, hypothesis: Dict[str,Any], data_patterns: Dict[str,Any]):
        base = hypothesis.get('confidence_initial', 0.5)
        adj = 0.0
        if data_patterns.get('consistent_trends'):
            adj += 0.1
        if data_patterns.get('large_sample_size'):
            adj += 0.05
        return round(min(1.0, base + adj), 2)
