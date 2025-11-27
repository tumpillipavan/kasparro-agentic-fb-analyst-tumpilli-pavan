class CreativeGenerator:
    def __init__(self, config=None):
        self.config = config or {}

    def generate_improvements(self, low_ctr_campaigns, high_performing_creatives):
        out = {"campaign_improvements": []}
        for c in low_ctr_campaigns:
            name = c.get('campaign_name', 'Unnamed')
            curr_ctr = float(c.get('ctr') or 0)
            new1 = {
                "creative_id":"C1",
                "headline":f"Limited Time: Save Big on {name}",
                "primary_text":"Experience superior comfort — limited stock. Shop now and get free shipping.",
                "call_to_action":"Shop Now",
                "expected_improvement":"CTR +25-50%",
                "testing_priority":"high",
                "rationale":"Adds urgency and clear value proposition"
            }
            new2 = {
                "creative_id":"C2",
                "headline":f"Why Customers Love {name}",
                "primary_text":"Loved by thousands — engineered for comfort. See what the hype is about.",
                "call_to_action":"Learn More",
                "expected_improvement":"CTR +15-30%",
                "testing_priority":"medium",
                "rationale":"Uses social proof and curiosity"
            }
            out["campaign_improvements"].append({
                "campaign_name": name,
                "current_performance": {"avg_ctr": curr_ctr, "issues_identified": ["low_ctr"]},
                "new_creatives": [new1, new2]
            })
        return out
