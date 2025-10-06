# **Ứng Dụng Phân Tích Tình Cảm Đa Ngôn Ngữ**

Đây là một ứng dụng web được xây dựng bằng Flask, có khả năng phân tích tình cảm của văn bản bằng Tiếng Việt và Tiếng Anh.

## **Các tính năng nổi bật**

* **Phân tích đa ngôn ngữ**: Hỗ trợ cả Tiếng Anh và Tiếng Việt.  
* **Sử dụng mô hình tiên tiến**:  
  * Tiếng Anh: Sử dụng mô hình [distilbert-base-uncased-finetuned-sst-2-english](https://huggingface.co/distilbert-base-uncased-finetuned-sst-2-english) (Sanh et al., 2019).  
  * Tiếng Việt: Sử dụng mô hình [PhoBERT](https://huggingface.co/vinai/phobert-base) (Nguyen & Tuan Nguyen, Findings 2020).
* **Tự động nhận diện ngôn ngữ**: Hệ thống tự động xác định ngôn ngữ đầu vào và chọn model phù hợp.  
* **Giao diện hiện đại**: Giao diện người dùng thân thiện, mượt mà được xây dựng với Tailwind CSS.  
* **Phản hồi trực quan (Tính năng sáng tạo)**:  
  * Kết quả được hiển thị cùng **emoji** tương ứng với cảm xúc.  
  * Thẻ kết quả **đổi màu** theo tình cảm (Xanh-Tích cực, Đỏ-Tiêu cực).  
  * Điểm tin cậy được thể hiện dưới dạng một **đồng hồ đo dạng tròn** (circular gauge) đẹp mắt.  
* **Clean Architecture**: Mã nguồn được tổ chức thành các lớp riêng biệt (giao diện, logic nghiệp vụ, hạ tầng) để dễ dàng bảo trì và mở rộng.
* **Triển khai dễ dàng với Docker**: Có thể chạy ứng dụng trong container Docker để đảm bảo tính nhất quán môi trường.

## **Cấu trúc thư mục**

.  
├── app.py                  \# File chính dùng để chạy ứng dụng Flask  
├── services/  
│   └── sentiment\_service.py  \# Chứa logic nghiệp vụ (nhận diện ngôn ngữ, gọi model)  
├── infrastructure/  
│   └── huggingface\_model.py  \# Lớp để tải và chạy model từ Hugging Face  
├── templates/  
│   └── index.html            \# File HTML giao diện người dùng  
├── requirements.txt        \# Các thư viện Python cần thiết  
└── README.md               \# File hướng dẫn

## **Hướng dẫn cài đặt và chạy ứng dụng**

1. **Tạo một môi trường ảo (khuyến khích):**  
   python \-m venv venv  
   source venv/bin/activate  \# Trên Windows: venv\\Scripts\\activate

2. **Cài đặt các thư viện cần thiết:**  
   pip install \-r requirements.txt

   *Lưu ý: Việc tải các model từ Hugging Face (lần đầu tiên) có thể mất một chút thời gian tùy thuộc vào tốc độ mạng của bạn.*  
3. **Chạy ứng dụng:**  
   flask run

   Hoặc chạy trực tiếp file app.py:  
   python app.py

4. Truy cập ứng dụng:  
   Mở trình duyệt và truy cập vào địa chỉ http://127.0.0.1:5000.

## **Đóng gói ứng dụng với Docker**

Chạy lệnh dưới đây để thực hiện build và chạy ứng dụng trong container Docker:

```docker-compose up -d```

## **Triển khai lên Production**

Sử dụng một máy chủ WSGI như Gunicorn:

```gunicorn \--workers 3 \--bind 0.0.0.0:8000 app:app```


## **References**
1. Sanh, V., Debut, L., Chaumond, J., & Wolf, T. (2019). DistilBERT, a distilled version of BERT: smaller, faster, cheaper and lighter. arXiv preprint arXiv:1910.01108.

2. [PhoBERT: Pre-trained language models for Vietnamese](https://aclanthology.org/2020.findings-emnlp.92/) (Nguyen & Tuan Nguyen, Findings 2020)