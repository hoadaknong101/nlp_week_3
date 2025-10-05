from flask import Flask, render_template, request, jsonify
from services.sentiment_service import analyze_sentiment, initialize_model
import logging

logging.basicConfig(level=logging.INFO)

initialize_model()

app = Flask(__name__)

@app.route('/')
def index():
    """
    Render trang chủ của ứng dụng.
    """
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """
    Endpoint API nhận văn bản và trả về kết quả phân tích tình cảm.
    """
    try:
        data = request.get_json()
        text = data.get('text', '')

        if not text.strip():
            return jsonify({'error': 'Vui lòng nhập văn bản để phân tích.'}), 400

        result = analyze_sentiment(text)
        
        if 'error' in result:
            return jsonify(result), 400
            
        logging.info(f"Phân tích thành công cho văn bản: '{text[:30]}...' -> {result}")
        return jsonify(result)

    except Exception as e:
        logging.error(f"Đã xảy ra lỗi trong quá trình phân tích: {e}", exc_info=True)
        return jsonify({'error': 'Đã có lỗi xảy ra ở máy chủ. Vui lòng thử lại.'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
