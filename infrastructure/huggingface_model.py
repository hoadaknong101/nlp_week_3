from transformers import pipeline
import logging

class SentimentModel:
    """
    Một lớp bao bọc để tải và chạy các model từ Hugging Face.
    Sử dụng lazy loading để chỉ tải model khi cần thiết.
    """
    _model = None
    _model_name = None

    def __init__(self, model_name: str):
        self._model_name = model_name
        self._load_model()

    def _load_model(self):
        """
        Tải pipeline phân tích tình cảm từ Hugging Face.
        Hàm này chỉ được gọi một lần.
        """
        if self._model is None:
            try:
                logging.info(f"Đang tải model: {self._model_name}...")
                self._model = pipeline(
                    "sentiment-analysis",
                    model=self._model_name
                )
                logging.info(f"Tải model {self._model_name} thành công!")
            except Exception as e:
                logging.error(f"Không thể tải model {self._model_name}. Lỗi: {e}", exc_info=True)
                # Dừng ứng dụng nếu không tải được model
                raise RuntimeError(f"Không thể tải model {self._model_name}") from e

    def predict(self, text: str):
        """
        Thực hiện dự đoán tình cảm trên văn bản đầu vào.
        """
        return self._model(text)
