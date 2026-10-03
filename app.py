# 1. Cài đặt các thư viện cần thiết
!pip install streamlit -q
!npm install localtunnel -q

# 2. Tạo file app.py chứa mã nguồn Streamlit
%%writefile app.py
import streamlit as st
import pandas as pd

# --- CẤU HÌNH TRANG ---
st.set_page_config(
    page_title="Tính Lãi Tiết Kiệm", 
    page_icon="🏦", 
    layout="wide"
)

# --- HÀM TÍNH TOÁN ---
def tinh_lai_suat(so_tien, lai_suat, thoi_gian, hinh_thuc_nhan_lai):
    """
    Hàm tính toán tiền lãi và tổng tiền
    Giả định: lãi suất nhập vào là %/năm, thời gian tính bằng tháng.
    """
    lai_suat_thang = (lai_suat / 100) / 12
    
    if hinh_thuc_nhan_lai == "Cuối kỳ":
        # Lãi đơn tính một lần vào cuối kỳ
        tien_lai = so_tien * (lai_suat / 100) * (thoi_gian / 12)
        tong_tien = so_tien + tien_lai
        lai_dinh_ki = 0 # Không có nhận lãi định kỳ
        
    elif hinh_thuc_nhan_lai == "Hàng tháng":
        # Nhận lãi đều đặn mỗi tháng
        lai_dinh_ki = so_tien * lai_suat_thang
        tien_lai = lai_dinh_ki * thoi_gian
        tong_tien = so_tien + tien_lai
        
    elif hinh_thuc_nhan_lai == "Hàng quý":
        # Nhận lãi 3 tháng một lần. Nếu số tháng không chia hết cho 3 thì tính theo số quý làm tròn xuống
        # (Ở đây ta tạm tính đơn giản: tổng lãi chia đều cho số quý)
        so_quy = thoi_gian // 3
        if so_quy == 0:
            lai_dinh_ki = 0
            tien_lai = so_tien * (lai_suat / 100) * (thoi_gian / 12) # Trả lãi cuối kì do chưa đủ 1 quý
        else:
            lai_dinh_ki = so_tien * (lai_suat / 100) * (3 / 12)
            tien_lai = lai_dinh_ki * so_quy
        tong_tien = so_tien + tien_lai
    
    return tien_lai, tong_tien, lai_dinh_ki

# --- GIAO DIỆN CHÍNH ---
st.title("🏦 Ứng Dụng Tính Lãi Suất Tiết Kiệm")
st.markdown("---")

# Tạo 2 cột: Cột trái để nhập liệu, Cột phải để hiển thị kết quả
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📝 Nhập Thông Tin")
    so_tien_str = st.text_input("1. Số tiền gốc (VNĐ)", value="100000000", help="Có thể nhập liền hoặc dùng dấu phẩy (VD: 100,000,000)")
    lai_suat = st.number_input("2. Lãi suất (%/năm)", min_value=0.1, value=5.5, step=0.1)
    thoi_gian = st.number_input("3. Thời gian gửi (Tháng)", min_value=1, value=12, step=1)
    hinh_thuc = st.selectbox("4. Hình thức nhận lãi", ["Cuối kỳ", "Hàng tháng", "Hàng quý"])
    
    btn_tinh = st.button("🚀 Tính Toán Lãi Suất", use_container_width=True, type="primary")

with col2:
    st.subheader("📊 Kết Quả Tính Toán")
    
    if btn_tinh:
        try:
            # Xử lý chuỗi tiền tệ
            so_tien = float(so_tien_str.replace(',', ''))
            if so_tien <= 0:
                st.error("Vui lòng nhập số tiền lớn hơn 0!")
            else:
                # Gọi hàm tính toán
                tien_lai, tong_tien, lai_dinh_ki = tinh_lai_suat(so_tien, lai_suat, thoi_gian, hinh_thuc)
                
                # Hiển thị bằng các thẻ Metric xịn xò của Streamlit
                col_m1, col_m2 = st.columns(2)
                with col_m1:
                    st.metric(label="Tổng Tiền Lãi", value=f"{tien_lai:,.0f} đ", delta=f"{lai_suat}%/năm")
                    if hinh_thuc != "Cuối kỳ":
                        chu_ky = "tháng" if hinh_thuc == "Hàng tháng" else "quý"
                        st.metric(label=f"Tiền Lãi Định Kỳ (mỗi {chu_ky})", value=f"{lai_dinh_ki:,.0f} đ")
                    else:
                        st.metric(label="Tiền Lãi Định Kỳ", value="0 đ", help="Nhận một lần vào cuối kỳ")
                        
                with col_m2:
                    st.metric(label="Tổng Số Tiền Nhận Được (Gốc + Lãi)", value=f"{tong_tien:,.0f} đ", delta="An toàn")
                    st.metric(label="Số Tiền Gốc Ban Đầu", value=f"{so_tien:,.0f} đ")
                    
                st.success("Tính toán hoàn tất! Vui lòng kiểm tra các chỉ số phía trên.")
                
        except ValueError:
            st.error("Lỗi: Vui lòng nhập số tiền hợp lệ!")
    else:
        st.info("👈 Nhập thông tin bên trái và bấm nút 'Tính Toán Lãi Suất' để xem kết quả.")

# 3. Chạy ứng dụng Streamlit ngầm và lấy địa chỉ IP công cộng (để nhập mật khẩu localtunnel)
import urllib
print("Bạn hãy click vào link có đuôi '.loca.lt' bên dưới.")
print("Khi trang web hiện ra, nó sẽ yêu cầu nhập 'Endpoint IP'.")
print("Hãy copy và dán dãy số IP dưới đây vào ô trống đó:")
!curl -s ipv4.icanhazip.com

# 4. Chạy Streamlit và mở cổng bằng Localtunnel
!streamlit run app.py & npx localtunnel --port 8501
