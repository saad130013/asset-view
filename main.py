import streamlit as st
import pandas as pd

st.set_page_config(page_title="نظام أصول الهيئة", layout="wide")
st.title("📊 نظام إدارة الأصول - الهيئة الجيولوجية السعودية")

uploaded_file = st.file_uploader("📂 حمّل ملف الأصول (Excel)", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file, header=1)
        df.columns = df.columns.str.strip()

        # عرض مربع البحث
        search_term = st.text_input("🔍 ابحث باسم الأصل أو رقمه").lower()

        if search_term:
            filtered_df = df[df.apply(
                lambda row: search_term in str(row.get("Asset Description For Maintenance Purpose", "")).lower()
                or search_term in str(row.get("Unique Asset Number in the entity", "")).lower(), axis=1)]

            if not filtered_df.empty:
                st.success(f"تم العثور على {len(filtered_df)} نتيجة")
                for _, asset in filtered_df.iterrows():
                    with st.expander(f"🖹 {asset['Asset Description For Maintenance Purpose']}"):
                        st.markdown(f"**📌 رقم الأصل:** {asset['Unique Asset Number in the entity']}")
                        st.markdown(f"**📍 المدينة / المنطقة:** {asset['City']} / {asset['Region']}")
                        st.markdown(f"**💰 التكلفة:** {asset['Cost']} ريال")
                        with st.container():
                            st.markdown("### 🧾 التفاصيل المحاسبية:")
                            st.markdown(f"- الاستهلاك المتراكم: {asset['Accumulated Depreciation']}")
                            st.markdown(f"- القيمة الدفترية: {asset['Net Book Value']}")
                            st.markdown(f"- العمر الإنتاجي: {asset['Useful Life']} سنوات")
            else:
                st.warning("لم يتم العثور على نتائج.")
        else:
            st.info("يرجى إدخال كلمة للبحث...")
    except Exception as e:
        st.error(f"حدث خطأ أثناء قراءة الملف: {str(e)}")
