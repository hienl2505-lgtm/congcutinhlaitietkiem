# Cài đặt Streamlit và Localtunnel
!pip install streamlit -q
!npm install localtunnel -q

# Tạo file app.py chứa mã nguồn giao diện Streamlit
%%writefile app.py
import streamlit as st

# Cấu hình trang
st.set_page_config(page_title="Tính Lãi Tiết Kiệm", page_icon="🏦", layout="wide")

st.title("🏦 Bảng Tính Lãi Suất Tiết Kiệm")
st.markdown("---")

# Chia bố cục làm 2 cột
col_input, col_output = st.columns([1, 2], gap="large")

with col_input:
    st.subheader("📝 Nhập thông tin")
    # Sử dụng format %f để hiển thị số lớn không bị dạng khoa học (e)
    so_tien_goc = st.number_input("Số tiền gốc (VNĐ)", min_value=0.0, value=100000000.0, step=1000000.0, format="%.0f")
    lai_suat = st.number_input("Lãi suất (%/năm)", min_value=0.0, value=6.0, step=0.1)
    ky_han = st.number_input("Kỳ hạn (tháng)", min_value=1, value=12, step=1)
    hinh_thuc = st.selectbox("Hình thức nhận lãi", ["Cuối kỳ", "Hàng tháng", "Hàng quý"])

# Xử lý logic tính toán
lai_suat_nam = lai_suat / 100
lai_suat_thang = lai_suat_nam / 12

lai_dinh_ky = 0
tong_lai = 0
can_hien_thi_canh_bao = False

if hinh_thuc == "Cuối kỳ":
    tong_lai = so_tien_goc * lai_suat_nam * (ky_han / 12)
    lai_dinh_ky = 0
elif hinh_thuc == "Hàng tháng":
    lai_dinh_ky = so_tien_goc * lai_suat_thang
    tong_lai = lai_dinh_ky * ky_han
elif hinh_thuc == "Hàng quý":
    so_quy = ky_han // 3
    lai_dinh_ky = so_tien_goc * lai_suat_nam / 4
    tong_lai = lai_dinh_ky * so_quy
    if ky_han % 3 != 0:
        can_hien_thi_canh_bao = True

tong_tien = so_tien_goc + tong_lai

with col_output:
    st.subheader("📊 Kết quả dự tính")
    
    # Hiển thị các chỉ số (Metrics) nổi bật
    m1, m2 = st.columns(2)
    m1.metric(label="Tổng Số Tiền Gốc", value=f"{so_tien_goc:,.0f} ₫")
    m2.metric(label="Lãi Suất Áp Dụng", value=f"{lai_suat}% / năm")
    
    m3, m4 = st.columns(2)
    if hinh_thuc == "Cuối kỳ":
        m3.metric(label="Tiền Lãi Định Kỳ", value="0 ₫", delta="Nhận 1 lần cuối kỳ", delta_color="off")
    else:
        chu_ky = "tháng" if hinh_thuc == "Hàng tháng" else "quý"
        m3.metric(label=f"Tiền Lãi Định Kỳ (mỗi {chu_ky})", value=f"{lai_dinh_ky:,.0f} ₫")
        
    m4.metric(label="Tổng Tiền Lãi (Cả kỳ)", value=f"{tong_lai:,.0f} ₫")
    
    # Khối hiển thị tổng tiền nổi bật
    st.success(f"### 💰 Tổng tiền nhận được (Gốc + Lãi): {tong_tien:,.0f} ₫")
    
    if can_hien_thi_canh_bao:
        st.warning("⚠️ Nhắc nhở: Kỳ hạn bạn chọn không tròn quý. Số tháng lẻ ra thường sẽ được ngân hàng áp dụng lãi suất không kỳ hạn (rất thấp), công cụ hiện chỉ tính tiền lãi cho các quý trọn vẹn.")
