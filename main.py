# app.py
import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# -- إعداد الصفحة --
st.set_page_config(
    page_title="نظام إدارة الأصول الذكي",
    layout="wide",
    page_icon="📊"
)

# -- أنماط CSS مخصصة --
st.markdown("""
    <style>
    .stApp {background-color: #f0f2f6;}
    .stTable {border: 1px solid #ddd; border-radius: 8px;}
    .stTextInput input {border-radius: 10px; padding: 8px;}
    .stSelectbox div {background-color: #fff; border-radius: 8px;}
    .warning {color: #cc0000; font-weight: bold;}
    </style>
""", unsafe_allow_html=True)

# -- تحميل البيانات --
try:
    df = pd.read_excel("assetv4.xlsx", header=1)
    df.columns = df.columns.str.strip()
except FileNotFoundError:
    st.error("❌ لم يتم العثور على ملف البيانات 'assetv4.xlsx'")
    st.stop()
except Exception as e:
    st.error(f"❌ خطأ في تحميل البيانات: {str(e)}")
    st.stop()

# -- التهيئة المسبقة --
descriptions_list = df['Asset Description For Maintenance Purpose'].dropna().tolist()
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(descriptions_list)

arabic_labels = {
    "Custodian": "المستلم", "Consolidated Code": "الرمز الموحد",
    "Unique Asset Number in MoF system": "الرقم الموحد في وزارة المالية",
    "Linked/Associated Asset": "الأصل المرتبط",
    "Unique Asset Number in the entity": "الرقم الموحد في الجهة",
    "Asset Description": "وصف الأصل", "Tag number": "رقم الوسم",
    "Base Unit of Measure": "وحدة القياس", "Quantity": "الكمية",
    "Manufacturer": "الشركة المصنعة", "Date Placed in Service": "تاريخ التشغيل",
    "Cost": "التكلفة", "Depreciation amount": "مبلغ الإهلاك",
    "Accumulated Depreciation": "الإهلاك المتراكم",
    "Residual Value": "القيمة المتبقية", "Net Book Value": "القيمة الدفترية",
    "Useful Life": "العمر الإنتاجي", "Remaining useful life": "العمر المتبقي",
    "Country": "الدولة", "Region": "المنطقة", "City": "المدينة",
    "Geographical Coordinates": "الإحداثيات الجغرافية",
    "National Address ID": "العنوان الوطني", "Building Number": "رقم المبنى",
    "Floors Number": "عدد الطوابق", "Room/office Number": "رقم الغرفة/المكتب"
}

# -- واجهة المستخدم --
tab1, tab2 = st.tabs(["🔎 البحث عن أصل", "🤖 التصنيف الذكي"])

with tab1:
    st.header("🔍 البحث عن أصل")
    search_input = st.text_input("... اكتب للبحث", key="search")
    
    if search_input:
        filtered = df[
            df["Asset Description For Maintenance Purpose"]
            .astype(str)
            .str.lower()
            .str.contains(search_input.lower(), na=False)
        ]
        
        if not filtered.empty:
            selected = st.selectbox(
                "اختر الأصل:",
                filtered["Asset Description For Maintenance Purpose"].unique(),
                format_func=lambda x: f"📄 {x}"
            )
            
            asset = filtered[filtered["Asset Description For Maintenance Purpose"] == selected].iloc[0]
            
            # جدول المعلومات
            general_data = {
                "المستلم": asset.get("Custodian", "—"),
                "الرمز الموحد": asset.get("Consolidated Code", "—"),
                "الرقم الموحد (وزارة المالية)": asset.get("Unique Asset Number in MoF system", "—"),
                "الكمية": asset.get("Quantity", "—"),
                "الشركة المصنعة": asset.get("Manufacturer", "—"),
                "التكلفة": f"{asset.get('Cost', 0):,.2f} ريال" if pd.notna(asset.get("Cost")) else "—",
            }
            
            st.table(pd.DataFrame(general_data.items(), columns=["الحقل", "القيمة"]))
            
            # الخريطة
            if "Geographical Coordinates" in asset and isinstance(asset["Geographical Coordinates"], str):
                try:
                    lat, lon = map(float, asset["Geographical Coordinates"].split(","))
                    st.map(pd.DataFrame({'lat': [lat], 'lon': [lon]}))
                except:
                    st.warning("⚠️ إحداثيات غير صحيحة")

        else:
            st.warning("🔍 لم يتم العثور على نتائج")

with tab2:
    st.header("🤖 التصنيف الذكي")
    user_desc = st.text_input("أدخل وصف الأصل", key="classify")
    
    if user_desc:
        try:
            user_vec = vectorizer.transform([user_desc])
            similarities = cosine_similarity(user_vec, tfidf_matrix).flatten()
            top_idx = similarities.argmax()
            
            match = df.iloc[top_idx]
            
            st.success(f"✅ أفضل تطابق ({similarities[top_idx]*100:.1f}%):")
            st.write(f"**{match['Asset Description For Maintenance Purpose']}**")
            
            # جدول التصنيف
            st.table(pd.DataFrame({
                "المستوى": ["التصنيف الرئيسي", "الفرعي", "المجموعة"],
                "الكود": [
                    match.get("Level 1 FA Module Code", "—"),
                    match.get("Level 2 FA Module Code", "—"),
                    match.get("accounting group Code", "—")
                ]
            }))
            
        except Exception as e:
            st.error(f"❌ خطأ في التصنيف: {str(e)}")

# -- تذييل الصفحة --
st.sidebar.markdown("""
    <div style="text-align: center; margin-top: 50px;">
        <p>تطوير: <a href="https://github.com/your-username">your-username</a></p>
    </div>
""", unsafe_allow_html=True)
