# PROJECT SPECIFICATION

## 1. THÔNG TIN ĐỀ TÀI

Tên đề tài:

**Phân tích xu hướng thất nghiệp và mối liên hệ với các yếu tố kinh tế – xã hội tại một số quốc gia châu Á giai đoạn 2010–2024**

Mục tiêu:

Phân tích diễn biến thất nghiệp tại một số quốc gia châu Á, so sánh giữa các quốc gia và nghiên cứu mối liên hệ giữa thất nghiệp với một số yếu tố kinh tế – xã hội.

---

## 2. PHẠM VI

### Quốc gia

Chỉ sử dụng 5 quốc gia:

* Việt Nam — VNM
* Thái Lan — THA
* Nhật Bản — JPN
* Hàn Quốc — KOR
* Philippines — PHL

### Thời gian

2010–2024.

Có thể chia thành:

* 2010–2019: trước COVID-19
* 2020–2021: giai đoạn COVID-19
* 2022–2024: giai đoạn phục hồi

Không tự ý mở rộng phạm vi nếu chưa có yêu cầu.

---

## 3. BIẾN DỮ LIỆU CHÍNH

Ưu tiên thu thập:

* Country
* Country_Code
* Year
* Unemployment_Rate
* Youth_Unemployment_Rate
* Male_Unemployment_Rate
* Female_Unemployment_Rate
* GDP_Growth
* GDP_per_Capita
* Inflation
* Labor_Force_Participation
* Population

Có thể bổ sung:

* Education_Level
* Education_Unemployment_Rate
* Urban_Unemployment_Rate
* Rural_Unemployment_Rate

Chỉ bổ sung khi có dữ liệu thực tế, đủ độ tin cậy và định nghĩa tương thích.

---

## 4. NGUỒN DỮ LIỆU

Ưu tiên:

1. World Bank
2. ILOSTAT / ILO
3. Our World in Data khi cần kiểm tra hoặc bổ sung phù hợp

Không sử dụng dữ liệu giả.

Không tự tạo số liệu để lấp khoảng trống.

Không tự suy đoán số liệu chưa có nguồn.

Mỗi biến phải có thông tin về nguồn và định nghĩa.

---

## 5. NGUYÊN TẮC DỮ LIỆU

Bắt buộc:

* Dữ liệu phải là dữ liệu thực.
* Không hard-code số liệu phân tích.
* Không tạo mock data để thay thế dữ liệu thật.
* Không tự ý thay missing value bằng số ngẫu nhiên.
* Không trộn các chỉ tiêu có định nghĩa khác nhau.
* Kiểm tra đơn vị đo.
* Kiểm tra năm.
* Kiểm tra quốc gia.
* Kiểm tra duplicate.
* Kiểm tra missing.
* Kiểm tra kiểu dữ liệu.
* Kiểm tra các giá trị bất thường.

Nếu một biến không có dữ liệu đáng tin cậy:

**Giữ missing hoặc loại biến đó khỏi phân tích. Không được bịa dữ liệu.**

---

## 6. CÂU HỎI NGHIÊN CỨU

Hệ thống cần hỗ trợ trả lời:

1. Tỷ lệ thất nghiệp thay đổi như thế nào trong giai đoạn 2010–2024?
2. Tỷ lệ thất nghiệp khác nhau như thế nào giữa 5 quốc gia?
3. COVID-19 có liên quan như thế nào đến biến động thất nghiệp?
4. GDP Growth có mối liên hệ như thế nào với thất nghiệp?
5. Inflation có mối liên hệ như thế nào với thất nghiệp?
6. Tỷ lệ thất nghiệp giữa nam và nữ có khác nhau không?
7. Thất nghiệp thanh niên khác thất nghiệp tổng thể như thế nào?
8. Nếu dữ liệu phù hợp, trình độ học vấn có mối liên hệ như thế nào với thất nghiệp?

---

## 7. PHÂN TÍCH

Các chỉ số có thể sử dụng:

* Mean
* Median nếu cần
* Minimum
* Maximum
* Standard deviation nếu phù hợp
* Change over time
* Gender gap
* Youth gap
* Pearson correlation khi điều kiện dữ liệu phù hợp

Công thức:

Gender Gap:

Female_Unemployment_Rate - Male_Unemployment_Rate

Youth Gap:

Youth_Unemployment_Rate - Unemployment_Rate

Correlation chỉ thể hiện:

**mối liên hệ thống kê**

Không được diễn giải correlation thành quan hệ nhân quả.

Không được viết:

"GDP tăng gây thất nghiệp giảm."

Có thể viết:

"Dữ liệu cho thấy GDP Growth và Unemployment Rate có mối tương quan..."

---

## 8. CÔNG NGHỆ

Sử dụng:

* Python
* Pandas
* NumPy
* SciPy
* Plotly
* Streamlit

Dữ liệu:

* CSV hoặc Parquet

---

## 9. CẤU TRÚC DỰ ÁN

```text
unemployment-dashboard/

├── PROJECT_SPEC.md
│
├── agents/
│   ├── agent_01_data_engineer.md
│   ├── agent_02_data_analyst.md
│   ├── agent_03_visualization.md
│   ├── agent_04_streamlit.md
│   └── agent_05_qa.md
│
├── data/
│   ├── raw/
│   └── processed/
│
├── analysis/
│
├── charts/
│
├── src/
│
├── app.py
├── requirements.txt
└── README.md
```

---

## 10. DASHBOARD

Dashboard sử dụng tỷ lệ màn hình 16:9.

Các thành phần chính:

### KPI

* Current/Selected Unemployment Rate
* Average Unemployment Rate
* Maximum Unemployment Year
* Average GDP Growth

### Biểu đồ

1. Unemployment Trend
2. Country Comparison
3. Country Map
4. GDP vs Unemployment
5. Gender Unemployment
6. Youth vs Overall Unemployment
7. Inflation vs Unemployment
8. Education nếu dữ liệu đủ

### Bộ lọc

* Country
* Year
* Period
* Gender
* Age Group nếu có dữ liệu

---

## 11. NGUYÊN TẮC BIỂU ĐỒ

* Time series → Line chart
* So sánh quốc gia → Bar chart
* So sánh giới tính → Grouped bar chart
* GDP vs unemployment → Scatter plot
* Inflation vs unemployment → Scatter plot
* Phân bố quốc gia → Choropleth map

Không sử dụng pie chart cho dữ liệu xu hướng theo thời gian.

Biểu đồ phải có:

* Title
* Axis
* Unit
* Legend nếu cần
* Tooltip
* Source khi phù hợp

Màu của cùng một quốc gia phải nhất quán giữa các biểu đồ.

---

## 12. PHÂN QUYỀN CỦA CÁC AGENT

### Agent 1

Chịu trách nhiệm:

**DATA**

Không làm dashboard.

### Agent 2

Chịu trách nhiệm:

**ANALYSIS**

Không tự thay dataset của Agent 1.

### Agent 3

Chịu trách nhiệm:

**VISUALIZATION**

Không tự tạo dữ liệu.

### Agent 4

Chịu trách nhiệm:

**STREAMLIT/UI**

Không thay đổi logic phân tích.

### Agent 5

Chịu trách nhiệm:

**QA + ACADEMIC REVIEW**

Không tự âm thầm sửa lỗi.

Nếu phát hiện lỗi nghiêm trọng, phải tạo báo cáo chỉ rõ Agent nào cần sửa.

---

## 13. HANDOFF

Luồng làm việc:

```text
Agent 1
   ↓
unemployment_final.csv
data_dictionary.csv
source_metadata.csv
   ↓
Agent 2
   ↓
analysis_results.csv
statistics.csv
findings.md
   ↓
Agent 3
   ↓
charts/
visualization_spec.md
   ↓
Agent 4
   ↓
app.py
dashboard
   ↓
Agent 5
   ↓
QA_REPORT.md
```

Nếu QA phát hiện lỗi:

```text
QA_REPORT.md
      ↓
Agent chịu trách nhiệm
      ↓
sửa
      ↓
chạy lại các bước phụ thuộc
      ↓
QA lại
```

Không được bỏ qua lỗi dữ liệu hoặc lỗi phương pháp luận.

---

## 14. NGUYÊN TẮC HỌC THUẬT

Dự án phải có khả năng giải thích khi bảo vệ.

Mọi lựa chọn quan trọng phải giải thích được:

* Vì sao chọn dữ liệu?
* Vì sao chọn 5 quốc gia?
* Vì sao chọn 2010–2024?
* Vì sao chọn biểu đồ này?
* Vì sao sử dụng Pearson correlation?
* Missing data xử lý thế nào?
* Các chỉ số có cùng định nghĩa không?
* Correlation có chứng minh causation không?

Không đưa ra kết luận vượt quá dữ liệu.

Không sử dụng các từ như "nguyên nhân", "gây ra", "tác động trực tiếp" nếu phân tích không chứng minh được quan hệ nhân quả.
