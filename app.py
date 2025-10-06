from flask import Flask, render_template, request, jsonify
from services.sentiment_service import analyze_sentiment, initialize_model
from services.crawl_data_reddit import reddit
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

@app.route('/analyze-url', methods=['POST'])
def analyze_social_post():
    """
    Phân tích tính tích cực và tiêu cực của một bài đăng trên mạng xã hội (Reddit).
    """
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({"error": "Vui lòng cung cấp URL."}), 400

    results = []
    try:
        submission = reddit.submission(url=url)
        submission.comments.replace_more(limit=0)
        comment_count = 0

        # Tăng giới hạn bình luận được phân tích
        COMMENT_LIMIT = 50 

        for comment in submission.comments.list():
            if comment_count >= COMMENT_LIMIT:
                break
            
            try:
                # Bỏ qua các bình luận quá ngắn hoặc đã bị xóa
                if not comment.body or comment.body == '[deleted]' or comment.body == '[removed]':
                    continue

                sentiment = analyze_sentiment(comment.body)

                if 'error' in sentiment:
                    logging.warning(f"Bình luận không thể phân tích: {comment.body[:30]}... Lỗi: {sentiment['error']}")
                    continue
                
                # Thêm cả author để có thể hiển thị nếu muốn
                results.append({
                    'author': str(comment.author),
                    'text': comment.body,
                    'sentiment': sentiment['label'],
                    'score': sentiment['score']
                })
            except Exception as e:
                logging.error(f"Lỗi khi phân tích bình luận: {e}", exc_info=True)
                continue
            
            comment_count += 1

        if not results:
             return jsonify({"error": "Không tìm thấy bình luận nào có thể phân tích."}), 404

        positive_count = sum(1 for r in results if r['sentiment'] == 'Tích cực')
        negative_count = sum(1 for r in results if r['sentiment'] == 'Tiêu cực')
        neutral_count = sum(1 for r in results if r['sentiment'] == 'Trung tính')
        total_count = len(results)

        summary = {
            "positive_percent": round((positive_count / total_count) * 100),
            "negative_percent": round((negative_count / total_count) * 100),
            "neutral_percent": round((neutral_count / total_count) * 100),
            "total_comments": total_count,
            "details": results 
        }

        return jsonify(summary)

    except Exception as e:
        logging.error(f"Lỗi nghiêm trọng khi xử lý URL: {e}", exc_info=True)
        return jsonify({"error": f"Không thể xử lý URL hoặc đã có lỗi xảy ra: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
