from flask import Flask
from extensions import csrf
from routes import sarimax_bp, exponencial_bp, session_bp
from config import Config

app = Flask(__name__)

# Carregar configurações
app.config.from_object(Config)

csrf.init_app(app)

# Registrar os blueprints para organizar as rotas
app.register_blueprint(sarimax_bp, url_prefix="/sarimax")
app.register_blueprint(exponencial_bp, url_prefix="/exponencial")
app.register_blueprint(session_bp, url_prefix="/session")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True) 