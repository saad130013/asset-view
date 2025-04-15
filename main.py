import streamlit as st
import pandas as pd

st.set_page_config(page_title="نظام إدارة الأصول", layout="wide")
st.title("📊 نظام إدارة الأصول - الهيئة الجيولوجية السعودية")

uploaded_file = st.file_uploader("📂 حمّل ملف الأصول (Excel)", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file, header=1)
        df.columns = df.columns.str.strip()

        # عرض مربع البحث لتصفية الخيارات
        search_input = st.text_input("🔍 ابحث باسم الأصل")

        # تصفية قائمة الأصول بناءً على ما يكتبه المستخدم
        filtered_options = df[
            df["Asset Description For Maintenance Purpose"].str.contains(search_input, case=False, na=False)
        ]["Asset Description For Maintenance Purpose"].unique().tolist()

        if filtered_options:
            selected_description = st.selectbox("📄 اختر الأصل من القائمة:", filtered_options)

            # عرض المعلومات العامة
            asset_row = df[df["Asset Description For Maintenance Purpose"] == selected_description].iloc[0]
            st.subheader("📌 المعلومات العامة")
            st.markdown(f"- **رقم الأصل:** {asset_row['Unique Asset Number in the entity']}")
            st.markdown(f"- **الموقع:** {asset_row['City']} / {asset_row['Region']}")
            st.markdown(f"- **التكلفة:** {asset_row['Cost']} ريال")

            # زر عرض التفاصيل المحاسبية
            if st.button("عرض التفاصيل المحاسبية"):
                st.subheader("🧾 التفاصيل المحاسبية")
                st.markdown(f"- الاستهلاك المتراكم: {asset_row['Accumulated Depreciation']}")
                st.markdown(f"- القيمة الدفترية: {asset_row['Net Book Value']}")
                st.markdown(f"- العمر الإنتاجي: {asset_row['Useful Life']} سنوات")
        else:
            if search_input:
                st.warning("لا توجد أصول مطابقة للبحث.")
    except Exception as e:
        st.error(f"❌ خطأ أثناء تحميل الملف: {str(e)}")
