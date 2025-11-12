from flask import Flask, request, jsonify
import pickle
import os
import time

app = Flask(__name__)

APP_VERSION = "0.1" # mudar isso depois para testar o CI/CD
MODEL_PATH = "model.pickle"

model = None
model_timestamp = 0

def load_model():
    global model, model_timestamp
    
    if not os.path.exists(MODEL_PATH):
        print(f"arquivo de modelo não encontrado em {MODEL_PATH}")
        return

    try:
        current_timestamp = os.path.getmtime(MODEL_PATH)
        if current_timestamp != model_timestamp:
            print(f"mudança no modelo")
            with open(MODEL_PATH, "rb") as f:
                model = pickle.load(f)
            model_timestamp = current_timestamp
            print(f"modelo carregado. data: {time.ctime(model_timestamp)}")
            
    except (IOError, pickle.PickleError, EOFError) as e:
        print(f"Erro ao carregar o modelo: {e}")
        model = None

@app.route("/api/recommend", methods=["POST"])
def recommend():
    load_model()
    
    if model is None:
        return jsonify({"error": "modelo não disponível ou inválido"}), 503

    data = request.get_json(force=True)
    if not data or 'songs' not in data:
        return jsonify({"error": "requisição inválida. 'songs' não encontrado."}), 400
        
    user_songs = data.get('songs', [])

    recommendations = ["Simulated-Song-1", "Simulated-Song-2"]

    response = {
        "songs": recommendations,
        "version": APP_VERSION,
        "model_date": time.ctime(model_timestamp) if model_timestamp > 0 else "N/A"
    }
    
    return jsonify(response)

if __name__ == "__main__":
    print("iniciando servidor flask")
    load_model() 

    app.run(host="0.0.0.0", port=5000, debug=True)
