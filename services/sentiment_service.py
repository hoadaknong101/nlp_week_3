from common import constant
from infrastructure.huggingface_model import SentimentModel
import logging
import langid

vi_model = None
eng_model = None

def initialize_model():
    """
    Khởi tạo model nếu chưa được khởi tạo.
    """
    global vi_model, eng_model

    logging.info("Khởi tạo các model phân tích tình cảm...")
    
    try:  
      vi_model = SentimentModel(constant.vietnamese_model)
      eng_model = SentimentModel(constant.english_model)
      
      logging.info("Khởi tạo model hoàn tất.")
    except Exception as e:
      logging.error(f"Lỗi khi khởi tạo model: {e}", exc_info=True)
      
      raise RuntimeError("Không thể khởi tạo các model phân tích tình cảm.") from e
  
    return vi_model, eng_model

def analyze_sentiment(text: str) -> dict:
    """
    Phân tích tình cảm của văn bản đầu vào.
    Tự động nhận diện ngôn ngữ và sử dụng model tương ứng.
    """
    if vi_model is None or eng_model is None:
      initialize_model()

    try:
        model = None
        lang = langid.classify(text)[0]
        detected_lang = None
        logging.info(f"Ngôn ngữ được nhận diện: {lang}")

        if lang == 'vi':
            model = vi_model
            detected_lang = "Tiếng Việt"
        elif lang == 'en':
            model = eng_model
            detected_lang = "Tiếng Anh"
        else:
            return {'error': f'Không nhận diện được ngôn ngữ.'}
        
        result = model.predict(text)
        label = result[0]['label'].upper()
        score = result[0]['score']

        sentiment_info = None
        if lang == 'vi':
            sentiment_info = constant.VIETNAMESE_SENTIMENT_MAP.get(label)
        else:
            sentiment_info = constant.ENGLISH_SENTIMENT_MAP.get(label)

        return {
            'language': detected_lang,
            'sentiment': sentiment_info["label"],
            'score': round(score * 100, 2),
            'emoji': sentiment_info["emoji"],
            'color': sentiment_info["color"]
        }
    except Exception as e:
        logging.error(f"Lỗi khi xử lý với model: {e}", exc_info=True)

        return {'error': 'Có lỗi xảy ra trong quá trình phân tích tình cảm.'}
