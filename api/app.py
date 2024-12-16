from flask import Flask, request, jsonify, render_template, Response
from tempfile import NamedTemporaryFile
from ultralytics import YOLO
from flasgger import Swagger
from flask_cors import CORS
from functools import wraps
from PIL import Image
import os

app = Flask(__name__)
swagger = Swagger(app)
CORS(app)

try:
    model = YOLO("best.pt")  
except Exception as e:
    print(f"Erro ao carregar o modelo YOLO: {e}")
    model = None

USERNAME = os.getenv("API_USERNAME", "admin")
PASSWORD = os.getenv("API_PASSWORD", "password123")

def check_auth(username, password):
    return username == USERNAME and password == PASSWORD

def authenticate():
    return Response(
        'Autenticação necessária. Por favor, forneça as credenciais.',
        401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'}
    )

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

def process_image(file):
    try:
        img = Image.open(file)
        if img.mode == 'RGBA': 
            img = img.convert('RGB')

        with NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
            img.save(tmp_file.name)
            return tmp_file.name

    except Exception as e:
        raise ValueError(f"Erro ao processar a imagem: {e}")

@app.route('/')
def index():
    """
    Página inicial da API.
    ---
    responses:
      200:
        description: Página HTML exibindo o formulário de upload.
    """
    return render_template('index.html')

@app.route('/classify', methods=['POST'])
@requires_auth
def predict():
    """
    Realiza a predição de uma imagem enviada.
    ---
    consumes:
      - multipart/form-data
    parameters:
      - name: image
        in: formData
        type: file
        required: true
        description: Imagem a ser processada pelo modelo.
    responses:
      200:
        description: Predição realizada com sucesso.
        schema:
          type: object
          properties:
            image_name:
              type: string
              example: "imagem.jpg"
            prediction:
              type: string
              example: "aberta"
            confidence:
              type: number
              example: 0.95
      400:
        description: Erro na requisição, como falta de imagem.
      401:
        description: Não autorizado. Credenciais inválidas ou ausentes. Verifique suas credenciais e tente novamente.
      500:
        description: Erro interno do servidor.
    description: |
      Este endpoint requer autenticação básica. As credenciais padrão são:
      
      - Usuário: `admin`
      - Senha: `password123`

      Caso tenha configurado variáveis de ambiente `API_USERNAME` e `API_PASSWORD`, use as credenciais personalizadas.

      A autenticação deve ser feita enviando um cabeçalho `Authorization` no formato:
      
      `"Basic <base64_credenciais>"`, onde `<base64_credenciais>` é a codificação em base64 de `usuário:senha`.

      Exemplo para autenticação básica:
      
      - "Basic YWRtaW46cGFzc3dvcmQxMjM=" (onde `admin:password123` é convertido para base64).
    """
    if 'image' not in request.files:
        return jsonify({"error": "Nenhuma imagem enviada"}), 400

    file = request.files['image']

    if not file.content_type.startswith('image'):
        return jsonify({"error": "O arquivo enviado não é uma imagem válida"}), 400

    try:
        original_filename = file.filename
        image_path = process_image(file)

        if model is None:
            return jsonify({"error": "Modelo YOLO não carregado"}), 500

        results = model.predict(image_path)

        result = results[0]
        class_names = result.names
        probs = result.probs.data.cpu().numpy()
        predicted_class_idx = probs.argmax()
        predicted_class = class_names[predicted_class_idx]
        confidence = float(probs[predicted_class_idx])

        class_mapping = {"open": "aberta", "close": "fechada"}
        result_mapped = class_mapping.get(predicted_class, "desconhecida")

        response = {
            "image_name": original_filename,
            "prediction": result_mapped,
            "confidence": confidence
        }

        return jsonify(response), 200

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400

    except Exception as e:
        return jsonify({"error": f"Erro inesperado: {str(e)}"}), 500

    finally:
        if os.path.exists(image_path):
            os.remove(image_path)



@app.route('/health')
def health_check():
    """
    Verifica o status da API.
    ---
    responses:
      200:
        description: API está funcional.
        schema:
          type: object
          properties:
            status:
              type: string
              example: "ok"
      500:
        description: Erro interno do servidor.
    """
    try:
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.getenv("FLASK_PORT", 5000))
    app.run(host='0.0.0.0', port=port)
