
import streamlit as st
import pandas as pd

st.set_page_config(page_title="نظام إدارة الأصول", layout="wide")
st.markdown("""
<style>
    body {
        background-color: #f8f9fa;
    }
    .main {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 10px;
    }
    .custom-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 15px;
    }
    .custom-table th {
        background-color: #007bff;
        color: white;
        padding: 10px;
        text-align: center;
    }
    .custom-table td {
        padding: 8px;
        text-align: center;
        border: 1px solid #dee2e6;
    }
    .custom-table tr:nth-child(even) {
        background-color: #f2f2f2;
    }
</style>
""", unsafe_allow_html=True)

st.title("📊 نظام إدارة الأصول - الهيئة الجيولوجية السعودية")

try:
    df = pd.read_excel("assetv4.xlsx", header=1)
    df.columns = df.columns.str.strip()

    search_input = st.text_input("🔍 ابحث باسم الأصل").strip().lower()

    filtered_options = df[
        df["Asset Description For Maintenance Purpose"].astype(str).str.lower().str.contains(search_input, na=False)
    ]["Asset Description For Maintenance Purpose"].dropna().unique().tolist()

    if filtered_options:
        selected_description = st.selectbox("📄 اختر الأصل من القائمة:", filtered_options)

        asset_row = df[df["Asset Description For Maintenance Purpose"] == selected_description].iloc[0]

        st.markdown("### 🧾 المعلومات العامة للأصل")
        general_fields = [
            "Asset Description For Maintenance Purpose", "Asset Functional Code", "GL account", "Cost Center",
            "Asset Owner", "Custodian", "Consolidated Code", "Unique Asset Number in MoF system",
            "Linked/Associated Asset", "Unique Asset Number in the entity", "Asset Description", "Tag number",
            "Base Unit of Measure", "Quantity", "Manufacturer", "Date Placed in Service", "Cost",
            "Depreciation amount", "Accumulated Depreciation", "Residual Value", "Net Book Value",
            "Useful Life", "Remaining useful life", "Country", "Region", "City", "Geographical Coordinates",
            "National Address ID", "Building Number", "Floors Number", "Room/office Number"
        ]
        general_data = {f"📝 {field}": asset_row.get(field, "غير متوفر") for field in general_fields}
        df_general = pd.DataFrame([(f"📝 {k}", v) for k, v in general_data.items()], columns=["🧾 اسم الحقل", "القيمة"])
        st.markdown(df_general.to_html(classes='custom-table', index=False, escape=False), unsafe_allow_html=True)

        if st.button("📘 عرض التفاصيل المحاسبية"):
            st.markdown("### 📚 التصنيفات المحاسبية")
            def get_safe(key):
                val = asset_row.get(key, "")
                return "غير متوفر" if pd.isna(val) or val == "" else val

            accounting_df = pd.DataFrame([
                ["🎯 " + get_safe("Level 1 FA Module Code"), get_safe("Level 1 FA Module - English Description"), get_safe("Level 1 FA Module - Arabic Description")],
                ["🏷️ " + get_safe("Level 2 FA Module Code"), get_safe("Level 2 FA Module - English Description"), get_safe("Level 2 FA Module - Arabic Description")],
                ["🔒 " + get_safe("Level 3 FA Module Code"), get_safe("Level 3 FA Module - English Description"), get_safe("Level 3 FA Module - Arabic Description")],
                ["💼 " + get_safe("accounting group Code"), get_safe("accounting group English Description"), get_safe("accounting group Arabic Description")],
                ["📦 " + get_safe("Asset Code For Accounting Purpose"), "Asset Code For Accounting Purpose", "—"]
            ], columns=["الكود", "الوصف بالإنجليزية", "الوصف بالعربية"])

            st.markdown(accounting_df.to_html(classes='custom-table', index=False, escape=False), unsafe_allow_html=True)

    elif search_input:
        st.warning("❌ لا توجد أصول مطابقة للبحث.")
except Exception as e:
    st.error(f"❌ حدث خطأ أثناء تحميل أو معالجة الملف: {str(e)}")
