import pandas as pd
from fpgrowth_py import fpgrowth
import pickle
import os

MODEL_DIR = "."
MODEL_PATH = os.path.join(MODEL_DIR, "model.pickle")

print("usando dados de simulação:")
itemSetList = [['eggs', 'bacon', 'soup'],
               ['eggs', 'bacon', 'apple'],
               ['soup', 'bacon', 'banana']]
print(f"total de 'playlists' de simulação: {len(itemSetList)}")

freqItemSet, rules = fpgrowth(itemSetList, minSupRatio=0.5, minConf=0.5)

os.makedirs(MODEL_DIR, exist_ok=True)

with open(MODEL_PATH, "wb") as f:
    pickle.dump(rules, f)
    
print(f"modelo salvo com sucesso em: {MODEL_PATH}")
print("regras geradas:")
print(rules)
