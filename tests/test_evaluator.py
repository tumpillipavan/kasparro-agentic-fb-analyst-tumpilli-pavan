import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from agents.evaluator import EvaluatorAgent


def test_init():
    ev = EvaluatorAgent()
    assert ev is not None

def test_confidence_calc():
    ev = EvaluatorAgent()
    c = ev.calculate_quantitative_confidence({'confidence_initial':0.6}, {'consistent_trends':True})
    assert 0.0 <= c <= 1.0
