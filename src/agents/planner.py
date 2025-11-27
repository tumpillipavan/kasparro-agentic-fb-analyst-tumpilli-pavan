from typing import Dict, Any

class PlannerAgent:
    def __init__(self, config=None):
        self.config = config or {}

    def plan_analysis(self, user_query: str) -> Dict[str, Any]:
        primary_metric = "roas"
        time_period = "last_30_days"
        q = user_query.lower()
        if "ctr" in q:
            primary_metric = "ctr"
        if "last 7" in q or "last 7 days" in q:
            time_period = "last_7_days"
        plan = {
            "query_analysis": {
                "primary_metric": primary_metric,
                "time_period": time_period,
                "comparison_type": "period_over_period"
            },
            "subtasks": [
                {"task_id":"data_loading","agent":"data_agent","description":"Load and summarize data","dependencies":[]},
                {"task_id":"trend_analysis","agent":"insight_agent","description":"Analyze trends for primary metric","dependencies":["data_loading"]},
                {"task_id":"validate","agent":"evaluator_agent","description":"Validate hypotheses","dependencies":["trend_analysis"]},
                {"task_id":"creative","agent":"creative_agent","description":"Generate creative ideas for low CTR campaigns","dependencies":["trend_analysis"]}
            ],
            "success_criteria":["identify_roas_drop_causes","generate_creative_recommendations"]
        }
        return plan
