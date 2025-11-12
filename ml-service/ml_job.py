import pandas as pd
from fpgrowth_py import fpgrowth
import pickle
import os

MODEL_DIR = "/app/model"
MODEL_PATH = os.path.join(MODEL_DIR, "model.pickle")

dataset_filename = os.getenv("DATASET_FILENAME")
if not dataset_filename:
    print("Erro: Variável de ambiente DATASET_FILENAME não definida")
    exit(1)

DATASET_PATH = os.path.join(MODEL_DIR, dataset_filename)
print(f"Carregando dataset de: {DATASET_PATH}")

try:
    df = pd.read_csv(DATASET_PATH)
    itemSetList = df.groupby('pid')['track_name'].apply(list).tolist()
    print(f"Total de playlists processadas: {len(itemSetList)}")
except FileNotFoundError:
    print(f"Erro: Arquivo de dataset não encontrado em {DATASET_PATH}")
    exit(1)
except Exception as e:
    print(f"Erro ao processar: {e}")
    exit(1)

print("Gerando regras com fpgrowth...")

freqItemSet, rules = fpgrowth(itemSetList, minSupRatio=0.01, minConf=0.1)

if not rules:
    print("Aviso: Nenhuma regra gerada com os parâmetros atuais. modelo vazio.")

with open(MODEL_PATH, "wb") as f:
    pickle.dump(rules, f)
    
print(f"Modelo salvo com sucesso em: {MODEL_PATH}")
