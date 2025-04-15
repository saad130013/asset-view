import streamlit as st
import pandas as pd

st.set_page_config(page_title="نظام إدارة الأصول", layout="wide")
st.title("📊 نظام إدارة الأصول - الهيئة الجيولوجية السعودية")

try:
    df = pd.read_excel("assetv4.xlsx", header=1)
    df.columns = df.columns.str.strip()

    search_input = st.text_input("🔍 ابحث باسم الأصل").strip().lower()

    filtered_options = df[
        df["Asset Description For Maintenance Purpose"].str.lower().str.contains(search_input, na=False)
    ]["Asset Description For Maintenance Purpose"].unique().tolist()

    if filtered_options:
        selected_description = st.selectbox("📄 اختر الأصل من القائمة:", filtered_options)

        asset_row = df[df["Asset Description For Maintenance Purpose"] == selected_description].iloc[0]
        st.subheader("📋 المعلومات العامة")
        general_html = """"""
        html_rows = ""
        for field in ['Asset Description For Maintenance Purpose', 'Asset Functional Code', 'GL account', 'Cost Center', 'Asset Owner', 'Custodian', 'Consolidated Code', 'Unique Asset Number in MoF system', 'Linked/Associated Asset', 'Unique Asset Number in the entity', 'Asset Description', 'Tag number', 'Base Unit of Measure', 'Quantity', 'Manufacturer', 'Date Placed in Service', 'Cost', 'Depreciation amount', 'Accumulated Depreciation', 'Residual Value', 'Net Book Value', 'Useful Life', 'Remaining useful life', 'Country', 'Region', 'City', 'Geographical Coordinates', 'National Address ID', 'Building Number', 'Floors Number', 'Room/office Number']:
            value = asset_row.get(field, "غير متوفر")
            html_rows += f"<tr><td>{field}</td><td>{value}</td></tr>"
        general_html = general_html.format(rows=html_rows)
        st.components.v1.html(general_html, height=700, scrolling=True)

        if st.button("عرض التفاصيل المحاسبية"):
            st.subheader("🧾 التصنيف المحاسبي")

            html_table = f'''
            <style>
                .styled-table {
                    border-collapse: collapse;
                    margin: 15px 0;
                    font-size: 16px;
                    min-width: 400px;
                    direction: rtl;
                    text-align: center;
                }
                .styled-table th,
                .styled-table td {
                    padding: 10px 20px;
                    border: 1px solid #ccc;
                }
                .styled-table th {
                    background-color: #f4f4f4;
                }
            </style>
            <table class="styled-table">
                <thead>
                    <tr>
                        <th>الكود</th><th>الوصف بالإنجليزية</th><th>الوصف بالعربية</th>
                    </tr>
                </thead>
                <tbody>
                    <tr><td>{asset_row.get("Level 1 FA Module Code")}</td><td>{asset_row.get("Level 1 FA Module - English Description")}</td><td>{asset_row.get("Level 1 FA Module - Arabic Description")}</td></tr>
                    <tr><td>{asset_row.get("Level 2 FA Module Code")}</td><td>{asset_row.get("Level 2 FA Module - English Description")}</td><td>{asset_row.get("Level 2 FA Module - Arabic Description")}</td></tr>
                    <tr><td>{asset_row.get("Level 3 FA Module Code")}</td><td>{asset_row.get("Level 3 FA Module - English Description")}</td><td>{asset_row.get("Level 3 FA Module - Arabic Description")}</td></tr>
                    <tr><td>{asset_row.get("accounting group Code")}</td><td>{asset_row.get("accounting group English Description")}</td><td>{asset_row.get("accounting group Arabic Description")}</td></tr>
                    <tr><td>{asset_row.get("Asset Code For Accounting Purpose")}</td><td colspan="2">كود الأصل المحاسبي</td></tr>
                </tbody>
            </table>
            '''
            st.components.v1.html(html_table, height=420, scrolling=True)
    else:
        if search_input:
            st.warning("لا توجد أصول مطابقة للبحث.")
except Exception as e:
    st.error(f"❌ خطأ أثناء تحميل أو معالجة الملف: {str(e)}")
