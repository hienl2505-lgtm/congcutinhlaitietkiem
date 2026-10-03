import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. CẤU HÌNH GIAO DIỆN ---
st.set_page_config(page_title="Công Cụ Tính Lãi Tiết Kiệm", page_icon="🏦", layout="wide")

# CSS tùy chỉnh để làm đẹp giao diện
st.markdown("""
    <style>
    .main-header {font-size: 2.5rem; font-weight: 700; color: #1E3A8A; text-align: center; margin-bottom: 0;}
    .sub-header {font-size: 1.2rem; color: #6B7280; text-align: center; margin-bottom: 2rem;}
    .metric-box {background-color: #F3F4F6; padding: 20px; border-radius: 10px; text-align: center; box-shadow: 2px 2px 5px rgba(0,0,0,0.05);}
    .metric-label {font-size: 1rem; color: #4B5563; margin-bottom: 5px;}
    .metric-value {font-size: 1.8rem; font-weight: 700; color: #059669;}
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">🏦 BẢNG TÍNH LÃI SUẤT TIẾT KIỆM</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Công cụ dự toán lợi nhuận chuyên nghiệp & trực quan</p>', unsafe_allow_html=True)

# --- 2. BỐ CỤC CHÍNH ---
col_input, col_output = st.columns([1.2, 2], gap="large")

with col_input:
    st.markdown("### 📝 Thông tin gửi tiền")
    with st.container(border=True):
        goc_input = st.number_input("💵 Tổng số tiền gốc (VNĐ)", min_value=1000000.0, value=100000000.0, step=10000000.0, format="%.0f")
        lai_suat_input = st.number_input("📈 Lãi suất (%/năm)", min_value=0.1, value=6.5, step=0.1)
        ky_han_input = st.number_input("⏱️ Kỳ hạn gửi (Tháng)", min_value=1, value=12, step=1)
        hinh_thuc_input = st.selectbox("🔄 Hình thức nhận lãi", ["Cuối kỳ", "Hàng tháng", "Hàng quý"])

# --- 3. XỬ LÝ LOGIC TOÁN HỌC ---
lai_suat_thap_phan = lai_suat_input / 100
tien_lai_dinh_ky = 0
tong_tien_lai = 0
lich_su_tra_lai = []

if hinh_thuc_input == "Cuối kỳ":
    tong_tien_lai = goc_input * lai_suat_thap_phan * (ky_han_input / 12)
    tien_lai_dinh_ky = 0
    lich_su_tra_lai.append({"Kỳ trả lãi": f"Tháng thứ {ky_han_input} (Cuối kỳ)", "Tiền gốc": goc_input, "Tiền lãi nhận": tong_tien_lai})

elif hinh_thuc_input == "Hàng tháng":
    tien_lai_dinh_ky = goc_input * (lai_suat_thap_phan / 12)
    tong_tien_lai = tien_lai_dinh_ky * ky_han_input
    for thang in range(1, int(ky_han_input) + 1):
        lich_su_tra_lai.append({"Kỳ trả lãi": f"Tháng thứ {thang}", "Tiền gốc": goc_input, "Tiền lãi nhận": tien_lai_dinh_ky})

elif hinh_thuc_input == "Hàng quý":
    tien_lai_dinh_ky = goc_input * (lai_suat_thap_phan / 4)
    so_quy = int(ky_han_input // 3)
    tong_tien_lai = tien_lai_dinh_ky * so_quy
    for quy in range(1, so_quy + 1):
        thang_nhan = quy * 3
        lich_su_tra_lai.append({"Kỳ trả lãi": f"Tháng thứ {thang_nhan} (Quý {quy})", "Tiền gốc": goc_input, "Tiền lãi nhận": tien_lai_dinh_ky})

tong_nhan = goc_input + tong_tien_lai

# --- 4. HIỂN THỊ KẾT QUẢ KHOA HỌC ---
with col_output:
    st.markdown("### 📊 Kết quả tính toán")
    
    # 4.1 Thẻ hiển thị số liệu nổi bật
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Tổng Số Tiền Gốc", f"{goc_input:,.0f} ₫")
    c2.metric("Lãi Suất", f"{lai_suat_input}%/năm")
    c3.metric("Tiền Lãi Định Kỳ", f"{tien_lai_dinh_ky:,.0f} ₫")
    c4.metric("Tổng Tiền Lãi", f"{tong_tien_lai:,.0f} ₫")
    
    st.markdown(f"""
        <div style="background-color: #D1FAE5; padding: 15px; border-radius: 10px; text-align: center; margin-top: 10px; border: 1px solid #34D399;">
            <h4 style="color: #065F46; margin: 0;">💰 TỔNG TIỀN NHẬN ĐƯỢC (GỐC + LÃI)</h4>
            <h2 style="color: #047857; margin: 5px 0 0 0;">{tong_nhan:,.0f} VNĐ</h2>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("---")
    
    # 4.2 Chia 2 tab: Biểu đồ và Lịch trả lãi
    tab1, tab2 = st.tabs(["🍩 Biểu đồ phân bổ", "📅 Lịch trả lãi chi tiết"])
    
    with tab1:
        # Vẽ biểu đồ Donut Chart bằng Plotly
        df_chart = pd.DataFrame({
            "Loại": ["Tiền Gốc", "Tiền Lãi"],
            "Giá trị": [goc_input, tong_tien_lai]
        })
        fig = px.pie(df_chart, values="Giá trị", names="Loại", hole=0.6, 
                     color="Loại", color_discrete_map={"Tiền Gốc": "#1E3A8A", "Tiền Lãi": "#10B981"})
        fig.update_traces(textposition='inside', textinfo='percent+label', 
                          hovertemplate="%{label}: %{value:,.0f} VNĐ")
        fig.update_layout(margin=dict(t=20, b=20, l=20, r=20), height=350, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        
    with tab2:
        # Bảng Dataframe lịch trả lãi
        if lich_su_tra_lai:
            df_lich = pd.DataFrame(lich_su_tra_lai)
            # Định dạng lại cột số tiền để có dấu phẩy
            df_lich["Tiền gốc"] = df_lich["Tiền gốc"].apply(lambda x: f"{x:,.0f} ₫")
            df_lich["Tiền lãi nhận"] = df_lich["Tiền lãi nhận"].apply(lambda x: f"{x:,.0f} ₫")
            st.dataframe(df_lich, use_container_width=True, hide_index=True)
        
        if hinh_thuc_input == "Hàng quý" and ky_han_input % 3 != 0:
            st.warning(f"⚠️ Kỳ hạn {ky_han_input} tháng bị lẻ. Công cụ chỉ tính lãi cho {int(ky_han_input//3)} quý trọn vẹn.")
