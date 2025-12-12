# ad_scoring.py
from typing import Dict

def score_ad(features: Dict[str, float]) -> float:
    """
    Simple example scoring:
    - base on CTR estimate, relevance and budget ratio
    features expected keys: 'ctr', 'relevance', 'budget_ratio'
    returns score between 0 and 100
    """
    ctr = float(features.get("ctr", 0.0))        # e.g., 0.02
    relevance = float(features.get("relevance", 0.0))  # 0..1
    budget_ratio = float(features.get("budget_ratio", 0.0))  # 0..1

    # Basic weighted formula
    score = (ctr * 1000) * 0.4 + (relevance * 100) * 0.5 + (budget_ratio * 100) * 0.1
    # clamp
    if score < 0:
        score = 0.0
    if score > 100.0:
        score = 100.0
    return round(score, 3)

if __name__ == "__main__":
    import json, sys
    # quick CLI: pass JSON features or default sample
    if len(sys.argv) > 1:
        features = json.loads(sys.argv[1])
    else:
        features = {"ctr": 0.02, "relevance": 0.8, "budget_ratio": 0.5}
    print(score_ad(features))
