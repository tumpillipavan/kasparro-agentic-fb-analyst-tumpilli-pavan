class InsightAgent:
    def __init__(self, config=None, use_llm=False):
        self.config = config or {}
        self.use_llm = use_llm

    def generate_hypotheses(self, data_summary, analysis_focus='ROAS drop'):
        hypotheses = []
        perf = data_summary.get('performance_metrics', {})
        avg_ctr = perf.get('avg_ctr') or 0
        avg_roas = perf.get('avg_roas') or 0

        if avg_ctr and avg_ctr < 0.02:
            hypotheses.append({
                "hypothesis_id":"H1",
                "description":"Audience fatigue or creative burnout causing low CTR",
                "reasoning":f"Average CTR {avg_ctr:.4f} is below threshold",
                "confidence_initial":0.6,
                "metrics_to_validate":["ctr_trend","frequency","roas_by_audience"]
            })
        if avg_roas and avg_roas < 1.5:
            hypotheses.append({
                "hypothesis_id":"H2",
                "description":"Low ROAS caused by low conversion rate or high CPC",
                "reasoning":f"Average ROAS {avg_roas:.2f} suggests poor spend efficiency",
                "confidence_initial":0.6,
                "metrics_to_validate":["roas_trend","cvr","cpc"]
            })
        if not hypotheses:
            hypotheses.append({
                "hypothesis_id":"H0",
                "description":"No strong signals from summary; need deeper analysis",
                "reasoning":"Metrics are within expected ranges",
                "confidence_initial":0.4,
                "metrics_to_validate":["detailed_time_series","creative_comparison"]
            })
        return {"hypotheses":hypotheses,"key_findings":{}}
