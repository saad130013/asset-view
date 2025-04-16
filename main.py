
import streamlit as st
import pandas as pd

st.set_page_config(page_title="نظام إدارة الأصول الذكي", layout="wide")
st.title("📊 نظام إدارة الأصول - الهيئة الجيولوجية السعودية")

# تحميل البيانات من ملف Excel
df = pd.read_excel("assetv4.xlsx", header=1)
df.columns = df.columns.str.strip()

# بناء قاعدة بيانات بسيطة من الوصف والتصنيفات
desc_df = df[[
    "Asset Description",
    "Level 1 FA Module - Arabic Description",
    "Level 2 FA Module - Arabic Description",
    "Level 3 FA Module - Arabic Description",
    "accounting group Arabic Description"
]].dropna().drop_duplicates()

# بناء قاعدة تصنيف
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

# إعداد التبويبات
tab1, tab2 = st.tabs(["🔎 البحث عن أصل", "🤖 التصنيف المحاسبي الذكي"])

# تبويب البحث عن أصل
with tab1:
    st.markdown("### 🔍 البحث عن أصل بالأسم أو الرقم")

    search_input = st.text_input("ادخل اسم أو رقم الأصل").strip().lower()
    if search_input:
        results = df[df["Asset Description For Maintenance Purpose"].astype(str).str.lower().str.contains(search_input)]
        if not results.empty:
            for _, row in results.iterrows():
                st.markdown(f"**🔹 الأصل:** {row['Asset Description For Maintenance Purpose']}")
                st.markdown(f"- الرقم: {row['Unique Asset Number in the entity']}")
                st.markdown(f"- الموقع: {row['City']} / {row['Region']}")
                st.markdown("---")
        else:
            st.warning("لم يتم العثور على نتائج.")

# تبويب التصنيف الذكي
with tab2:
    st.markdown("### 🤖 تصنيف محاسبي تلقائي")
    user_desc = st.text_input("✍️ أدخل وصف الأصل").strip().lower()
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
