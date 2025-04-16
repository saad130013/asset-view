
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

tab1, tab2 = st.tabs(["🔎 البحث عن أصل", "🤖 التصنيف المحاسبي الذكي"])

with tab1:
    

    # تعريف المسميات بالعربية
    arabic_labels = {
        "Custodian": "المستلم",
        "Consolidated Code": "الرمز الموحد",
        "Unique Asset Number in MoF system": "الرقم الموحد في وزارة المالية",
        "Linked/Associated Asset": "الأصل المرتبط",
        "Unique Asset Number in the entity": "الرقم الموحد في الجهة",
        "Asset Description": "وصف الأصل",
        "Tag number": "رقم الوسم",
        "Base Unit of Measure": "وحدة القياس",
        "Quantity": "الكمية",
        "Manufacturer": "الشركة المصنعة",
        "Date Placed in Service": "تاريخ التشغيل",
        "Cost": "التكلفة",
        "Depreciation amount": "مبلغ الإهلاك",
        "Accumulated Depreciation": "الإهلاك المتراكم",
        "Residual Value": "القيمة المتبقية",
        "Net Book Value": "القيمة الدفترية",
        "Useful Life": "العمر الإنتاجي",
        "Remaining useful life": "العمر المتبقي",
        "Country": "الدولة",
        "Region": "المنطقة",
        "City": "المدينة",
        "Geographical Coordinates": "الإحداثيات الجغرافية",
        "National Address ID": "العنوان الوطني",
        "Building Number": "رقم المبنى",
        "Floors Number": "عدد الطوابق",
        "Room/office Number": "رقم الغرفة / المكتب"
    }

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
                "Custodian", "Consolidated Code", "Unique Asset Number in MoF system",
                "Linked/Associated Asset", "Unique Asset Number in the entity", "Asset Description", "Tag number",
                "Base Unit of Measure", "Quantity", "Manufacturer", "Date Placed in Service", "Cost",
                "Depreciation amount", "Accumulated Depreciation", "Residual Value", "Net Book Value",
                "Useful Life", "Remaining useful life", "Country", "Region", "City",
                "Geographical Coordinates", "National Address ID", "Building Number", "Floors Number", "Room/office Number"
            ]

            general_data = {field: asset_row.get(field) for field in general_fields if pd.notna(asset_row.get(field)) and asset_row.get(field) != "Not Available"}

            # استخراج الإحداثيات وفصلها عن باقي الجدول
            geo = general_data.pop("Geographical Coordinates", None)

            df_general = pd.DataFrame([(f"📝 " + arabic_labels.get(k.strip(), k.strip()), v)
                                       for k, v in general_data.items()],
                                      columns=["🧾 اسم الحقل", "القيمة"])
            st.markdown(df_general.to_html(classes='custom-table', index=False, escape=False), unsafe_allow_html=True)

            if geo and isinstance(geo, str) and "," in geo:
                lat_lon = geo.split(",")
                if len(lat_lon) == 2:
                    try:
                        lat, lon = float(lat_lon[0]), float(lat_lon[1])
                        st.markdown("### 🗺️ موقع الأصل على الخريطة")
                        st.map(pd.DataFrame({'lat': [lat], 'lon': [lon]}))
                    except ValueError:
                        st.warning("⚠️ لم يتم عرض الخريطة: صيغة الإحداثيات غير صحيحة.")

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



with tab2:
st.markdown("### 🤖 تصنيف محاسبي تلقائي باستخدام الذكاء الصناعي")
    user_desc = st.text_input("✍️ أدخل وصف الأصل").strip().lower()
    
    # بناء قاعدة مبسطة من الملف
    desc_df = df[[
        "Asset Description",
        "Level 1 FA Module - Arabic Description",
        "Level 2 FA Module - Arabic Description",
        "Level 3 FA Module - Arabic Description",
        "accounting group Arabic Description"
    ]].dropna().drop_duplicates()

    classification_map = {}
    for _, row in desc_df.iterrows():
        words = str(row["Asset Description"]).strip().lower().split()
        for word in words:
            if word not in classification_map:
                classification_map[word] = {
                    "Level 1": row["Level 1 FA Module - Arabic Description"],
                    "Level 2": row["Level 2 FA Module - Arabic Description"],
                    "Level 3": row["Level 3 FA Module - Arabic Description"],
                    "Group": row["accounting group Arabic Description"]
                }

    if user_desc:
        found = False
        for word in user_desc.split():
            if word in classification_map:
                result = classification_map[word]
                st.success("✅ تم التعرف على التصنيف:")
                st.markdown(f"- **المستوى 1:** {result['Level 1']}")
                st.markdown(f"- **المستوى 2:** {result['Level 2']}")
                st.markdown(f"- **المستوى 3:** {result['Level 3']}")
                st.markdown(f"- **المجموعة المحاسبية:** {result['Group']}")
                found = True
                break
        if not found:
            st.error("❌ لا يمكن تحديد التصنيف بناءً على هذا الوصف.")