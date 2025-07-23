import json
import os

def load_etf_data():
    with open(os.path.join(os.path.dirname(__file__), '../data/etf_holdings.json'), 'r', encoding='utf-8') as f:
        return json.load(f)
