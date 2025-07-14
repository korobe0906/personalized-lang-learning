
# personalized-lang-learning  
**Tên ngắn gọn**: aim2lang  

## Mục tiêu dự án

`aim2lang` là một hệ thống tạo nội dung học ngoại ngữ được cá nhân hóa, sử dụng mô hình ngôn ngữ lớn (LLM), ontology từ vựng và kỹ thuật sinh prompt linh hoạt.  
Dự án cho phép người học nhập vào một mục tiêu học cụ thể (AIM), hệ thống sẽ phân tích và sinh ra bài học phù hợp theo ngữ cảnh, từ khóa và độ khó tương ứng.

---

## Thành phần chính

- **AIM Parser**: Trích xuất chủ đề và từ khóa từ mục tiêu học mà người dùng nhập vào.
- **Ontology Keywords**: Bộ từ khóa học thuật được tổ chức theo chủ đề (ví dụ: sân bay, nhà hàng, phỏng vấn).
- **Prompt Generator**: Tạo prompt dựa trên từ khóa phù hợp, đảm bảo chất lượng đầu vào cho LLM.
- **GPT Client**: Giao tiếp với OpenAI API để sinh ra nội dung bài học phù hợp (ví dụ: đoạn hội thoại).
- **Output Handler**: Lưu trữ và hiển thị kết quả học.

---

## Cấu trúc thư mục

personalized-lang-learning/
├── data/ # Dữ liệu ontology, ví dụ AIM
├── prompts/ # Template prompt cho GPT
├── src/ # Source code chính: parser, GPT client
├── output/ # Kết quả demo đầu ra
├── run_demo.py # Chạy demo đầu cuối
├── .env # Chứa API Key 
├── .gitignore # File để ignore các dữ liệu nhạy cảm
├── requirements.txt # Danh sách thư viện cần thiết
├── README.md # Tài liệu mô tả dự án

---

## Cách chạy demo

### 1. Cài thư viện cần thiết

pip install -r requirements.txt


### 2. Tạo file `.env` chứa OpenAI API key

Tạo file `.env` trong thư mục gốc với nội dung:

OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx


### 3. Chạy chương trình

python run_demo.py

Nhập một mục tiêu học ngoại ngữ, ví dụ:
Tôi muốn luyện hội thoại khi làm thủ tục tại sân bay


Chương trình sẽ phân tích chủ đề, tạo prompt, gửi đến GPT, và trả lại một đoạn hội thoại học tiếng Anh phù hợp.

---

## Ví dụ đầu ra

**AIM**:
Tôi muốn luyện hội thoại khi check-in ở sân bay

**Prompt gửi GPT**:
Viết đoạn hội thoại tiếng Anh cấp độ sơ cấp về tình huống: airport.
Dùng các từ khóa sau: check-in, boarding pass, passport, security.
Đảm bảo đơn giản, thực tế, không quá 5 câu.


**Kết quả từ GPT**:
A: Good morning. Where is the check-in desk?
B: Over there. Do you have your passport?
A: Yes, here it is.
B: Thank you. Here is your boarding pass.
A: Great, thanks!

---

## Ghi chú

- Hiện tại hệ thống sử dụng ontology đơn giản từ file JSON, có thể mở rộng thành cơ sở dữ liệu tri thức (RDF, OWL).
- Prompt có thể tối ưu thêm bằng kỹ thuật chain-of-thought hoặc RAG.
- Kết quả có thể dùng làm phần mô tả nội dung học trong app di động hoặc hệ thống học tập thực tế.

---

## Mở rộng

Dự án này có thể phát triển theo hướng:

- Tích hợp trong app học ngoại ngữ cá nhân hóa
- Viết bài báo khoa học ứng dụng LLM trong giáo dục
- Dự thi các startup competition về edtech
- Kết nối với hệ thống theo dõi tiến độ học và adaptive learning

---

## Bản quyền & liên hệ

Tác giả: KieuDiem  
Liên hệ: laptrinh0906@gmail.com 
Mục đích học thuật và demo cá nhân. Không sử dụng cho mục đích thương mại nếu chưa được cho phép.