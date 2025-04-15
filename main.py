import streamlit as st
import pandas as pd

st.set_page_config(page_title="نظام إدارة الأصول", layout="wide")
st.title("📊 نظام إدارة الأصول - الهيئة الجيولوجية السعودية")

uploaded_file = st.file_uploader("📂 حمّل ملف الأصول مع التصنيفات المحاسبية (Excel)", type=["xlsx"])

if uploaded_file:
    try:
        # قراءة الملف من الصف الثاني
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
                st.subheader("🧾 التفاصيل المحاسبية")
                st.markdown(f"- **كود الأصل المحاسبي:** {asset_row['Asset Code For Accounting Purpose']}")
                st.markdown(f"- **المجموعة المحاسبية:** {asset_row['accounting group Arabic Description']} ({asset_row['accounting group Code']})")
                st.markdown("### 🧩 التصنيفات المحاسبية:")
                st.markdown(f"- **المستوى 1:** {asset_row['Level 1 FA Module - Arabic Description']} ({asset_row['Level 1 FA Module Code']})")
                st.markdown(f"- **المستوى 2:** {asset_row['Level 2 FA Module - Arabic Description']} ({asset_row['Level 2 FA Module Code']})")
                st.markdown(f"- **المستوى 3:** {asset_row['Level 3 FA Module - Arabic Description']} ({asset_row['Level 3 FA Module Code']})")
        else:
            if search_input:
                st.warning("لا توجد أصول مطابقة للبحث.")
    except Exception as e:
        st.error(f"❌ خطأ أثناء تحميل أو معالجة الملف: {str(e)}")
