
import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="نظام إدارة الأصول الذكي", layout="wide")
st.title("📊 نظام إدارة الأصول - الهيئة الجيولوجية السعودية")

# تحميل البيانات
df = pd.read_excel("assetv4.xlsx", header=1)
df.columns = df.columns.str.strip()

# إعداد البيانات لـ TF-IDF
asset_descriptions = df["Asset Description For Maintenance Purpose"].dropna().astype(str).unique()
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(asset_descriptions)
descriptions_list = asset_descriptions.tolist()

# تعريب الحقول
arabic_labels = {
    "Custodian": "المستلم", "Consolidated Code": "الرمز الموحد", "Unique Asset Number in MoF system": "الرقم الموحد في وزارة المالية",
    "Linked/Associated Asset": "الأصل المرتبط", "Unique Asset Number in the entity": "الرقم الموحد في الجهة",
    "Asset Description": "وصف الأصل", "Tag number": "رقم الوسم", "Base Unit of Measure": "وحدة القياس",
    "Quantity": "الكمية", "Manufacturer": "الشركة المصنعة", "Date Placed in Service": "تاريخ التشغيل",
    "Cost": "التكلفة", "Depreciation amount": "مبلغ الإهلاك", "Accumulated Depreciation": "الإهلاك المتراكم",
    "Residual Value": "القيمة المتبقية", "Net Book Value": "القيمة الدفترية", "Useful Life": "العمر الإنتاجي",
    "Remaining useful life": "العمر المتبقي", "Country": "الدولة", "Region": "المنطقة", "City": "المدينة",
    "Geographical Coordinates": "الإحداثيات الجغرافية", "National Address ID": "العنوان الوطني",
    "Building Number": "رقم المبنى", "Floors Number": "عدد الطوابق", "Room/office Number": "رقم الغرفة / المكتب"
}

# تبويبات
tab1, tab2 = st.tabs(["🔍 البحث عن أصل", "🤖 التصنيف المحاسبي الذكي"])

# تبويب البحث
with tab1:
    try:
        search_input = st.text_input("🔍 ابحث باسم الأصل").strip().lower()
        filtered_options = df[
            df["Asset Description For Maintenance Purpose"].astype(str).str.lower().str.contains(search_input, na=False)
        ]["Asset Description For Maintenance Purpose"].dropna().unique().tolist()

        if filtered_options:
            selected_description = st.selectbox("📄 اختر الأصل من القائمة:", filtered_options, key="select_asset_desc")
            asset_row = df[df["Asset Description For Maintenance Purpose"] == selected_description].iloc[0]

            general_fields = [
                "Custodian", "Consolidated Code", "Unique Asset Number in MoF system",
                "Linked/Associated Asset", "Unique Asset Number in the entity", "Asset Description", "Tag number",
                "Base Unit of Measure", "Quantity", "Manufacturer", "Date Placed in Service", "Cost",
                "Depreciation amount", "Accumulated Depreciation", "Residual Value", "Net Book Value",
                "Useful Life", "Remaining useful life", "Country", "Region", "City",
                "Geographical Coordinates", "National Address ID", "Building Number", "Floors Number", "Room/office Number"
            ]

            general_data = {field: asset_row.get(field) for field in general_fields if pd.notna(asset_row.get(field)) and asset_row.get(field) != "Not Available"}
            geo = general_data.pop("Geographical Coordinates", None)

            st.subheader("📋 المعلومات العامة")
            table_data = [(f"📝 {arabic_labels.get(k, k)}", v) for k, v in general_data.items()]
            st.table(pd.DataFrame(table_data, columns=["🧾 اسم الحقل", "القيمة"]))

            if geo and isinstance(geo, str) and "," in geo:
                try:
                    lat, lon = map(float, geo.split(","))
                    st.markdown("### 🗺️ موقع الأصل على الخريطة")
                    st.map(pd.DataFrame({'lat': [lat], 'lon': [lon]}))
                except:
                    st.warning("⚠️ لم يتم عرض الخريطة: صيغة الإحداثيات غير صحيحة.")

            if st.button("📘 عرض التفاصيل المحاسبية"):
                def get_safe(key):
                    val = asset_row.get(key, "")
                    return "غير متوفر" if pd.isna(val) or val == "" else val

                accounting_df = pd.DataFrame([
                    ["🎯 " + get_safe("Level 1 FA Module Code"), get_safe("Level 1 FA Module - Arabic Description"), "المستوى 1"],
                    ["🏷️ " + get_safe("Level 2 FA Module Code"), get_safe("Level 2 FA Module - Arabic Description"), "المستوى 2"],
                    ["🔒 " + get_safe("Level 3 FA Module Code"), get_safe("Level 3 FA Module - Arabic Description"), "المستوى 3"],
                    ["💼 " + get_safe("accounting group Code"), get_safe("accounting group Arabic Description"), "المجموعة المحاسبية"],
                    ["📦 " + get_safe("Asset Code For Accounting Purpose"), "Asset Code For Accounting Purpose", "الكود النهائي"]
                ], columns=["الكود", "الوصف بالعربية", "المستوى"])
                st.table(accounting_df)

        elif search_input:
            st.warning("❌ لا توجد أصول مطابقة للبحث.")
    except Exception as e:
        st.error(f"❌ حدث خطأ أثناء تحميل أو معالجة الملف: {str(e)}")

# تبويب التصنيف الذكي

# تبويب التصنيف الذكي
with tab2:
    st.markdown("### 🧠 أدخل وصف الأصل لتحديد التصنيف تلقائيًا")
    user_desc = st.text_input("✍️ وصف الأصل")

    if user_desc:
        # اقتراحات فورية
        user_vec = vectorizer.transform([user_desc])
        similarities = cosine_similarity(user_vec, tfidf_matrix)
        top_indices = similarities.argsort()[0][-5:][::-1]  # أفضل 5 أوصاف

        suggestions = [descriptions_list[i] for i in top_indices if similarities[0][i] > 0][:3]  # أعلى 3 فقط

        if suggestions:
            st.markdown("#### 💡 اقتراحات مشابهة:")
            for s in suggestions:
                st.markdown(f"- {s}")

        # التصنيف باستخدام أعلى وصف مطابق
        top_index = similarities.argmax()
        top_desc = descriptions_list[top_index]
        match_row = df[df["Asset Description For Maintenance Purpose"] == top_desc].iloc[0]

        table_data = [
            ["🎯 " + str(match_row.get("Level 1 FA Module Code", "—")), match_row.get("Level 1 FA Module - Arabic Description", "—"), "المستوى 1"],
            ["🏷️ " + str(match_row.get("Level 2 FA Module Code", "—")), match_row.get("Level 2 FA Module - Arabic Description", "—"), "المستوى 2"],
            ["🔒 " + str(match_row.get("Level 3 FA Module Code", "—")), match_row.get("Level 3 FA Module - Arabic Description", "—"), "المستوى 3"],
            ["💼 " + str(match_row.get("accounting group Code", "—")), match_row.get("accounting group Arabic Description", "—"), "المجموعة المحاسبية"],
            ["📦 " + str(match_row.get("Asset Code For Accounting Purpose", "—")), "Asset Code For Accounting Purpose", "الكود النهائي"]
        ]
        st.markdown("### 📘 نتيجة التصنيف")
        st.table(pd.DataFrame(table_data, columns=["الكود", "الوصف بالعربية", "المستوى"]))

    if user_desc:
        user_vec = vectorizer.transform([user_desc])
        similarities = cosine_similarity(user_vec, tfidf_matrix)
        top_index = similarities.argmax()
        top_desc = descriptions_list[top_index]
        match_row = df[df["Asset Description For Maintenance Purpose"] == top_desc].iloc[0]

        table_data = [
            ["🎯 " + str(match_row.get("Level 1 FA Module Code", "—")), match_row.get("Level 1 FA Module - Arabic Description", "—"), "المستوى 1"],
            ["🏷️ " + str(match_row.get("Level 2 FA Module Code", "—")), match_row.get("Level 2 FA Module - Arabic Description", "—"), "المستوى 2"],
            ["🔒 " + str(match_row.get("Level 3 FA Module Code", "—")), match_row.get("Level 3 FA Module - Arabic Description", "—"), "المستوى 3"],
            ["💼 " + str(match_row.get("accounting group Code", "—")), match_row.get("accounting group Arabic Description", "—"), "المجموعة المحاسبية"],
            ["📦 " + str(match_row.get("Asset Code For Accounting Purpose", "—")), "Asset Code For Accounting Purpose", "الكود النهائي"]
        ]
        st.markdown("### 📘 نتيجة التصنيف")
        st.table(pd.DataFrame(table_data, columns=["الكود", "الوصف بالعربية", "المستوى"]))