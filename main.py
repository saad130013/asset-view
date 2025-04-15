import streamlit as st
import pandas as pd

st.set_page_config(page_title="نظام إدارة الأصول", layout="wide")
st.title("📊 نظام إدارة الأصول - الهيئة الجيولوجية السعودية")

uploaded_file = st.file_uploader("📂 حمّل ملف الأصول مع التصنيفات المحاسبية (Excel)", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file, header=1)
        df.columns = df.columns.str.strip()

        search_input = st.text_input("🔍 ابحث باسم الأصل").strip().lower()

        filtered_options = df[
            df["Asset Description For Maintenance Purpose"].str.lower().str.contains(search_input, na=False)
        ]["Asset Description For Maintenance Purpose"].unique().tolist()

        if filtered_options:
            selected_description = st.selectbox("📄 اختر الأصل من القائمة:", filtered_options)

            asset_row = df[df["Asset Description For Maintenance Purpose"] == selected_description].iloc[0]
            st.subheader("📌 المعلومات العامة")
            st.markdown(f"- **رقم الأصل:** {asset_row['Unique Asset Number in the entity']}")
            st.markdown(f"- **الموقع:** {asset_row['City']} / {asset_row['Region']}")
            st.markdown(f"- **التكلفة:** {asset_row['Cost']} ريال")

            if st.button("عرض التفاصيل المحاسبية"):
                st.subheader("🧾 التصنيف المحاسبي")
                html_table = f"""
<style>
    .styled-table {{
        border-collapse: collapse;
        margin: 15px 0;
        font-size: 16px;
        min-width: 400px;
        direction: rtl;
        text-align: center;
    }}
    .styled-table th,
    .styled-table td {{
        padding: 10px 20px;
        border: 1px solid #ccc;
    }}
    .styled-table th {{
        background-color: #f4f4f4;
    }}
</style>
<table class="styled-table">
    <thead>
        <tr>
            <th>الكود</th>
            <th>الوصف بالإنجليزية</th>
            <th>الوصف بالعربية</th>
        </tr>
    </thead>
    <tbody>
        <tr><td>{{level1_code}}</td><td>{{level1_en}}</td><td>{{level1_ar}}</td></tr>
        <tr><td>{{level2_code}}</td><td>{{level2_en}}</td><td>{{level2_ar}}</td></tr>
        <tr><td>{{level3_code}}</td><td>{{level3_en}}</td><td>{{level3_ar}}</td></tr>
        <tr><td>{{group_code}}</td><td>{{group_en}}</td><td>{{group_ar}}</td></tr>
        <tr><td>{{asset_code}}</td><td colspan="2">كود الأصل المحاسبي</td></tr>
    </tbody>
</table>
"""
                html_table = html_table.format(
                    level1_code=asset_row['Level 1 FA Module Code'],
                    level1_en=asset_row['Level 1 FA Module - English Description'],
                    level1_ar=asset_row['Level 1 FA Module - Arabic Description'],
                    level2_code=asset_row['Level 2 FA Module Code'],
                    level2_en=asset_row['Level 2 FA Module - English Description'],
                    level2_ar=asset_row['Level 2 FA Module - Arabic Description'],
                    level3_code=asset_row['Level 3 FA Module Code'],
                    level3_en=asset_row['Level 3 FA Module - English Description'],
                    level3_ar=asset_row['Level 3 FA Module - Arabic Description'],
                    group_code=asset_row['accounting group Code'],
                    group_en=asset_row['accounting group English Description'],
                    group_ar=asset_row['accounting group Arabic Description'],
                    asset_code=asset_row['Asset Code For Accounting Purpose']
                )
                st.components.v1.html(html_table, height=420, scrolling=True)
        else:
            if search_input:
                st.warning("لا توجد أصول مطابقة للبحث.")
    except Exception as e:
        st.error(f"❌ خطأ أثناء تحميل أو معالجة الملف: {str(e)}")
