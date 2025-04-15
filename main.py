
import streamlit as st
import pandas as pd

st.set_page_config(page_title="نظام إدارة الأصول", layout="wide")
st.title("📊 نظام إدارة الأصول - الهيئة الجيولوجية السعودية")

try:
    df = pd.read_excel("assetv4.xlsx", header=1)
    df.columns = df.columns.str.strip()

    search_input = st.text_input("🔍 ابحث باسم الأصل").strip().lower()

    # تصفية الأصول المطابقة
    filtered_options = df[
        df["Asset Description For Maintenance Purpose"].astype(str).str.lower().str.contains(search_input, na=False)
    ]["Asset Description For Maintenance Purpose"].dropna().unique().tolist()

    if filtered_options:
        selected_description = st.selectbox("📄 اختر الأصل من القائمة:", filtered_options)

        asset_row = df[df["Asset Description For Maintenance Purpose"] == selected_description].iloc[0]

        # عرض المعلومات العامة في جدول
        st.subheader("📋 المعلومات العامة")
        general_fields = [
            "Asset Description For Maintenance Purpose", "Asset Functional Code", "GL account", "Cost Center",
            "Asset Owner", "Custodian", "Consolidated Code", "Unique Asset Number in MoF system",
            "Linked/Associated Asset", "Unique Asset Number in the entity", "Asset Description", "Tag number",
            "Base Unit of Measure", "Quantity", "Manufacturer", "Date Placed in Service", "Cost",
            "Depreciation amount", "Accumulated Depreciation", "Residual Value", "Net Book Value",
            "Useful Life", "Remaining useful life", "Country", "Region", "City", "Geographical Coordinates",
            "National Address ID", "Building Number", "Floors Number", "Room/office Number"
        ]
        general_data = {field: asset_row.get(field, "غير متوفر") for field in general_fields}
        st.table(pd.DataFrame(general_data.items(), columns=["اسم الحقل", "القيمة"]))

        # زر لعرض المعلومات المحاسبية
        if st.button("عرض التفاصيل المحاسبية"):
            st.subheader("🧾 التصنيف المحاسبي")
            accounting_fields = {
                "Level 1": {
                    "Code": asset_row.get("Level 1 FA Module Code", "غير متوفر"),
                    "Arabic": asset_row.get("Level 1 FA Module - Arabic Description", "غير متوفر"),
                    "English": asset_row.get("Level 1 FA Module - English Description", "غير متوفر"),
                },
                "Level 2": {
                    "Code": asset_row.get("Level 2 FA Module Code", "غير متوفر"),
                    "Arabic": asset_row.get("Level 2 FA Module - Arabic Description", "غير متوفر"),
                    "English": asset_row.get("Level 2 FA Module - English Description", "غير متوفر"),
                },
                "Level 3": {
                    "Code": asset_row.get("Level 3 FA Module Code", "غير متوفر"),
                    "Arabic": asset_row.get("Level 3 FA Module - Arabic Description", "غير متوفر"),
                    "English": asset_row.get("Level 3 FA Module - English Description", "غير متوفر"),
                },
                "Group": {
                    "Code": asset_row.get("accounting group Code", "غير متوفر"),
                    "Arabic": asset_row.get("accounting group Arabic Description", "غير متوفر"),
                    "English": asset_row.get("accounting group English Description", "غير متوفر"),
                },
                "Asset Code": {
                    "Code": asset_row.get("Asset Code For Accounting Purpose", "غير متوفر"),
                    "Arabic": "—",
                    "English": "Asset Code For Accounting Purpose"
                }
            }

            # تحويلها لجدول
            accounting_df = pd.DataFrame([
                [v["Code"], v["English"], v["Arabic"]] for k, v in accounting_fields.items()
            ], columns=["الكود", "الوصف بالإنجليزية", "الوصف بالعربية"])

            st.table(accounting_df)

    else:
        if search_input:
            st.warning("لا توجد أصول مطابقة للبحث.")

except Exception as e:
    st.error(f"❌ حدث خطأ أثناء تحميل أو معالجة الملف: {str(e)}")
