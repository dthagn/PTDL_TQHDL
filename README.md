# Phân tích Xu hướng Thất nghiệp Châu Á 2010-2024

Dashboard tương tác để phân tích xu hướng thất nghiệp và mối liên hệ với các yếu tố kinh tế – xã hội tại 5 quốc gia châu Á giai đoạn 2010–2024.

## Giới thiệu

Đây là ứng dụng dashboard tương tác được xây dựng với Streamlit để phân tích và trực quan hóa dữ liệu thất nghiệp tại 5 quốc gia châu Á:
- Nhật Bản (Japan)
- Philippines
- Hàn Quốc (South Korea)
- Thái Lan (Thailand)
- Việt Nam (Vietnam)

Phân tích bao gồm giai đoạn 2010-2024, chia thành 3 giai đoạn:
- Trước COVID-19 (2010-2019)
- COVID-19 (2020-2021)
- Phục hồi (2022-2024)

## Công nghệ

- **Python 3.8+**
- **Streamlit** - Framework dashboard tương tác
- **Pandas** - Xử lý dữ liệu
- **Plotly** - Trực quan hóa tương tác
- **NumPy** - Tính toán số học

## Cấu trúc dự án

```
unemployment-dashboard/
├── PROJECT_SPEC.md              # Đặc tả dự án
├── app.py                       # Ứng dụng Streamlit chính
├── requirements.txt             # Dependencies
├── README.md                    # Tài liệu này
├── src/                         # Module hỗ trợ
│   ├── data_loader.py          # Tải dữ liệu từ CSV
│   ├── preprocessing.py         # Xử lý và lọc dữ liệu
│   ├── visualization.py         # Tạo biểu đồ Plotly
│   └── dashboard_utils.py       # Hàm tiện ích dashboard
├── data/                        # Thư mục dữ liệu
│   ├── raw/                    # Dữ liệu thô
│   └── processed/              # Dữ liệu đã xử lý
│       ├── unemployment_final.csv
│       ├── data_dictionary.csv
│       └── source_metadata.csv
├── analysis/                    # Kết quả phân tích
│   ├── statistics.csv
│   ├── analysis_results.csv
│   ├── correlation_results.csv
│   └── findings.md
└── charts/                      # Scripts tạo biểu đồ
    ├── unemployment_trend.py
    ├── country_comparison.py
    ├── unemployment_map.py
    ├── gdp_unemployment.py
    ├── inflation_unemployment.py
    └── youth_unemployment.py
```

## Cài đặt

### Yêu cầu hệ thống
- Python 3.8 hoặc cao hơn
- pip (package manager)

### Bước 1: Clone hoặc tải dự án

```bash
cd PTDL&TQHDL
```

### Bước 2: Tạo môi trường ảo (khuyến nghị)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Bước 3: Cài đặt dependencies

```bash
pip install -r requirements.txt
```

## Cách chạy

### Chạy dashboard

```bash
streamlit run app.py
```

Dashboard sẽ mở tại `http://localhost:8501` trong trình duyệt của bạn.

### Tùy chọn chạy khác

```bash
# Chạy với port khác
streamlit run app.py --server.port 8502

# Chạy ở chế độ development
streamlit run app.py --logger.level debug
```

## Nguồn dữ liệu

Tất cả dữ liệu được lấy từ World Bank API:

- **Tỷ lệ thất nghiệp tổng thể**: World Bank Indicator `SL.UEM.TOTL.ZS`
- **Tỷ lệ thất nghiệp thanh niên**: World Bank Indicator `SL.UEM.1524.ZS`
- **Tăng trưởng GDP**: World Bank Indicator `NY.GDP.MKTP.KD.ZG`
- **GDP bình quân đầu người**: World Bank Indicator `NY.GDP.PCAP.CD`
- **Lạm phát**: World Bank Indicator `FP.CPI.TOTL.ZG`
- **Tỷ lệ tham gia lực lượng lao động**: World Bank Indicator `SL.TLF.CACT.ZS`
- **Dân số**: World Bank Indicator `SP.POP.TOTL`

**Lưu ý**: Dữ liệu thất nghiệp sử dụng ước tính mô hình hóa của ILO.

## Phương pháp

### Các chỉ số phân tích
- Trung bình (Mean)
- Trung vị (Median)
- Giá trị nhỏ nhất/tối đa (Min/Max)
- Độ lệch chuẩn (Standard Deviation)
- Thay đổi theo thời gian
- Youth Gap (Chênh lệch thanh niên)
- Hệ số tương quan Pearson (Pearson Correlation)

### Công thức

**Youth Gap:**
```
Youth Gap = Youth_Unemployment_Rate - Unemployment_Rate
```

**Hệ số tương quan Pearson:**
```
r = Σ((Xi - X̄)(Yi - Ỹ)) / √(Σ(Xi - X̄)² × Σ(Yi - Ỹ)²)
```

### Phân loại giai đoạn
- **Trước COVID-19 (2010-2019)**: Giai đoạn bình thường
- **COVID-19 (2020-2021)**: Giai đoạn đại dịch
- **Phục hồi (2022-2024)**: Giai đoạn phục hồi

## Tính năng Dashboard

### Điều hướng
- **Tổng quan**: KPI cards và biểu đồ tổng quan
- **Xu hướng theo thời gian**: Biểu đồ xu hướng thất nghiệp
- **So sánh quốc gia**: So sánh giữa các quốc gia
- **GDP & Thất nghiệp**: Phân tích tương quan GDP - Thất nghiệp
- **Lạm phát**: Phân tích tương quan Lạm phát - Thất nghiệp
- **Thanh niên**: Phân tích thất nghiệp thanh niên
- **Phân tích theo giai đoạn**: So sánh 3 giai đoạn
- **Dữ liệu**: Xem dữ liệu thô và thống kê
- **Phương pháp**: Chi tiết phương pháp phân tích
- **Kết luận**: Kết quả phân tích và hạn chế

### Bộ lọc
- **Quốc gia**: Chọn một hoặc nhiều quốc gia
- **Năm**: Chọn một hoặc nhiều năm
- **Giai đoạn**: Chọn giai đoạn thời gian

Tất cả biểu đồ và KPI được cập nhật động dựa trên bộ lọc.

### Biểu đồ
- **Line chart**: Xu hướng theo thời gian
- **Bar chart**: So sánh quốc gia và giai đoạn
- **Scatter plot**: Phân tích tương quan
- **Choropleth map**: Bản đồ địa lý
- **Grouped bar chart**: So sánh thanh niên vs tổng thể

## Giới hạn dữ liệu

1. **Dữ liệu giới tính**: Tỷ lệ thất nghiệp theo giới tính (nam/nữ) không có sẵn do yêu cầu xác thực API của ILOSTAT và hạn chế của API World Bank cho các quốc gia này.

2. **Dữ liệu trình độ học vấn**: Các biến liên quan đến trình độ học vấn không được đưa vào bộ dữ liệu cuối cùng do không có sẵn đáng tin cậy cho tất cả các quốc gia.

3. **Phạm vi thời gian**: Phân tích giới hạn trong giai đoạn 2010-2024. Không thể đánh giá xu hướng dài hạn.

4. **Tương quan vs Nhân quả**: Tất cả các phân tích tương quan chỉ cho thấy mối quan hệ thống kê. Không thể đưa ra kết luận về quan hệ nhân quả dựa trên dữ liệu này.

5. **Kích thước mẫu**: Các tương quan ở cấp quốc gia dựa trên chỉ 15 điểm dữ liệu cho mỗi quốc gia, làm hạn chế sức mạnh thống kê.

6. **Các yếu tố bên ngoài**: Phân tích không tính đến các yếu tố kinh tế, xã hội hoặc chính sách khác có thể ảnh hưởng đến thất nghiệp.

7. **Nguồn dữ liệu**: Tất cả dữ liệu đến từ ước tính của World Bank. Các ước tính mô hình hóa của ILO được sử dụng cho thất nghiệp và tỷ lệ tham gia lực lượng lao động, có thể có những hạn chế vốn có.

8. **Phạm vi địa lý**: Chỉ có 5 quốc gia châu Á được đưa vào. Kết quả có thể không tổng quát hóa cho các khu vực khác.

9. **Định nghĩa biến**: Tất cả các biến sử dụng định nghĩa của World Bank. Các định nghĩa khác nhau có thể cho ra kết quả khác nhau.

## Câu hỏi nghiên cứu

Dashboard hỗ trợ trả lời các câu hỏi sau:

1. Tỷ lệ thất nghiệp thay đổi như thế nào trong giai đoạn 2010–2024?
2. Tỷ lệ thất nghiệp khác nhau như thế nào giữa 5 quốc gia?
3. COVID-19 có liên quan như thế nào đến biến động thất nghiệp?
4. GDP Growth có mối liên hệ như thế nào với thất nghiệp?
5. Inflation có mối liên hệ như thế nào với thất nghiệp?
6. Tỷ lệ thất nghiệp giữa nam và nữ có khác nhau không? (Không có dữ liệu)
7. Thất nghiệp thanh niên khác thất nghiệp tổng thể như thế nào?
8. Trình độ học vấn có mối liên hệ như thế nào với thất nghiệp? (Không có dữ liệu)

## Ghi chú quan trọng

- **Không có dữ liệu giả**: Tất cả số liệu là dữ liệu thực từ World Bank
- **Không hard-code**: Tất cả KPI và biểu đồ được tính toán động từ dữ liệu
- **Tương quan ≠ Nhân quả**: Kết quả tương quan chỉ phản ánh mối quan hệ thống kê, không chứng minh quan hệ nhân quả
- **Phạm vi giới hạn**: Kết quả chỉ áp dụng cho 5 quốc gia và giai đoạn thời gian được phân tích

## Phát triển

Dự án này được phát triển theo quy trình multi-agent:
- **Agent 1**: Data Engineer - Thu thập và xử lý dữ liệu
- **Agent 2**: Data Analyst - Phân tích thống kê
- **Agent 3**: Visualization - Tạo biểu đồ
- **Agent 4**: Streamlit Developer - Xây dựng dashboard
- **Agent 5**: QA & Academic Review - Kiểm tra chất lượng

## Giấy phép

Dự án này được tạo ra cho mục đích học thuật và nghiên cứu.

## Liên hệ

Để biết thêm thông tin, vui lòng xem `PROJECT_SPEC.md` cho đặc tả chi tiết của dự án.
