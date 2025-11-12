from flask import Flask, request, jsonify
import pickle
import os
import time

app = Flask(__name__)

APP_VERSION = "0.2" 
MODEL_PATH = "/app/model/model.pickle"

model = None
model_timestamp = 0

def load_model():
    global model, model_timestamp
    
    if not os.path.exists(MODEL_PATH):
        print(f"Aviso: Arquivo de modelo não encontrado em {MODEL_PATH}")
        return

    try:
        current_timestamp = os.path.getmtime(MODEL_PATH)
        if current_timestamp != model_timestamp:
            print(f"Detectada mudança no modelo. Carregando...")
            with open(MODEL_PATH, "rb") as f:
                model = pickle.load(f)
            model_timestamp = current_timestamp
            print(f"Modelo carregado. Data: {time.ctime(model_timestamp)}")
            
    except Exception as e:
        print(f"Erro ao carregar o modelo: {e}")
        model = None

@app.route("/api/recommend", methods=["POST"])
def recommend():
    load_model()
    
    if model is None:
        return jsonify({"error": "Modelo não disponível ou inválido"}), 503

    data = request.get_json(force=True)
    if not data or 'songs' not in data:
        return jsonify({"error": "Requisição inválida. 'songs' não encontrado."}), 400
        
    user_songs = set(data.get('songs', []))
    recommendations = set()

    for antecedent, consequent, confidence in model:
        if set(antecedent).issubset(user_songs):
            recommendations.update(consequent)

    final_recommendations = list(recommendations - user_songs)

    response = {
        "songs": final_recommendations[:20], 
        "version": APP_VERSION,
        "model_date": time.ctime(model_timestamp) if model_timestamp > 0 else "N/A"
    }
    
    return jsonify(response)

if __name__ == "__main__":
    print("Iniciando servidor Flask (DADOS REAIS)...")
    load_model() 
    app.run(host="0.0.0.0", port=5000)
