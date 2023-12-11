import pandas as pd

with open('.\expirements\prediction_eval_results.csv', 'r') as f:
    lines = f.readlines()

print(lines[0].strip().split(','))