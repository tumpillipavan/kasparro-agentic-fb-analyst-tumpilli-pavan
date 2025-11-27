import json, os
from datetime import datetime
from src.agents.planner import PlannerAgent
from src.agents.data_agent import DataAgent
from src.agents.insight_agent import InsightAgent
from src.agents.evaluator import EvaluatorAgent
from src.agents.creative_generator import CreativeGenerator


class AgentOrchestrator:
    def __init__(self, config):
        self.config = config
        data_path = config.get('data_paths', {}).get('full') or config.get('data_paths', {}).get('sample')
        self.planner = PlannerAgent(config)
        self.data_agent = DataAgent(data_path)
        self.insight_agent = InsightAgent(config)
        self.evaluator_agent = EvaluatorAgent(config)
        self.creative_generator = CreativeGenerator(config)

    def execute_analysis(self, user_query):
        execution_id = f"exec_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        results = {'execution_id': execution_id, 'user_query': user_query, 'steps': {}}
        plan = self.planner.plan_analysis(user_query)
        results['steps']['planning'] = plan
        self.data_agent.load_data()
        summary = self.data_agent.generate_summary()
        results['steps']['data_summary'] = summary
        insights = self.insight_agent.generate_hypotheses(summary)
        results['steps']['insights'] = insights
        hypotheses = insights.get('hypotheses', [])
        validation = self.evaluator_agent.validate_hypotheses(hypotheses, summary)
        results['steps']['validation'] = validation
        low_ctr = self.data_agent.get_low_ctr_campaigns(self.config.get('thresholds', {}).get('low_ctr', 0.02))
        high_perf = self.data_agent.get_high_performing_creatives()
        creative_imp = self.creative_generator.generate_improvements(low_ctr, high_perf)
        results['steps']['creative_improvements'] = creative_imp
        results['final_report'] = {
            'executive_summary': {
                'overall_confidence': validation.get('overall_confidence', 0.5),
                'key_insights_count': len(validation.get('validated_hypotheses', [])),
                'creative_recommendations_count': len(creative_imp.get('campaign_improvements', []))
            },
            'top_recommendations': validation.get('validated_hypotheses', [])[:3],
            'creative_opportunities': creative_imp.get('campaign_improvements', [])
        }
        os.makedirs('logs', exist_ok=True)
        with open(os.path.join('logs', f'run_{execution_id}.json'), 'w') as f:
            json.dump({'summary': results['final_report']}, f, indent=2)
        return results
