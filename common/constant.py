# Tên model Hugging Face cho từng ngôn ngữ
vietnamese_model = "5CD-AI/Vietnamese-Sentiment-visobert"
english_model = "distilbert-base-uncased-finetuned-sst-2-english"

# Dictionary thông tin hiển thị
VIETNAMESE_SENTIMENT_MAP = {
    "POS": {"label": "Tích cực", "emoji": "😊", "color": "bg-green-100 text-green-800 border-green-400"},
    "NEG": {"label": "Tiêu cực", "emoji": "😠", "color": "bg-red-100 text-red-800 border-red-400"},
    "NEU": {"label": "Trung tính", "emoji": "😐", "color": "bg-blue-100 text-blue-800 border-blue-400"},
}
ENGLISH_SENTIMENT_MAP = {
    "POSITIVE": {"label": "Tích cực", "emoji": "😊", "color": "bg-green-100 text-green-800 border-green-400"},
    "NEGATIVE": {"label": "Tiêu cực", "emoji": "😠", "color": "bg-red-100 text-red-800 border-red-400"},
    "NEU": {"label": "Trung tính", "emoji": "😐", "color": "bg-blue-100 text-blue-800 border-blue-400"},
}

COMMENT_LIMIT = 50