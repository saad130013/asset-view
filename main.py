import streamlit as st
import pandas as pd
import torch
from sklearn.metrics.pairwise import cosine_similarity
from transformers import AutoTokenizer, AutoModel

# ========== إعداد التطبيق الأساسي ==========
st.set_page_config(
    page_title="🦉 النظام الذكي لاقتراح الأصول",
    page_icon="🏢",
    layout="wide"
)

# ========== تنسيق CSS مخصص ==========
st.markdown("""
<style>
    .stTextInput input {
        border: 2px solid #2e86c1 !important;
        border-radius: 10px;
        padding: 12px;
    }
    .stMarkdown h3 {
        color: #27ae60;
        border-bottom: 2px solid #3498db;
    }
    .result-card {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# ========== تحميل البيانات ==========
@st.cache_data
def load_data():
    try:
        df = pd.read_excel("assetv4.xlsx", header=1)
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"🚨 خطأ في تحميل الملف: {str(e)}")
        st.stop()

df = load_data()
asset_descriptions = df["Asset Description For Maintenance Purpose"].dropna().astype(str).unique().tolist()

# ========== تحميل النموذج ==========
@st.cache_resource
def load_bert_model():
    try:
        tokenizer = AutoTokenizer.from_pretrained("asafaya/bert-base-arabic")
        model = AutoModel.from_pretrained("asafaya/bert-base-arabic")
        return tokenizer, model
    except Exception as e:
        st.error(f"🤖 خطأ في تحميل النموذج: {str(e)}")
        st.stop()

tokenizer, model = load_bert_model()

# ========== توليد التضمينات ==========
@st.cache_data
def generate_embeddings():
    embeddings = []
    for desc in asset_descriptions:
        try:
            inputs = tokenizer(desc, return_tensors="pt", truncation=True, padding=True, max_length=32)
            with torch.no_grad():
                outputs = model(**inputs)
            embedding = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
            embeddings.append(embedding)
        except:
            embeddings.append([0.0]*768)
    return embeddings

embeddings = generate_embeddings()

# ========== واجهة المستخدم ==========
st.title("🤖 نظام اقتراح الأصول باستخدام BERT العربي")
user_input = st.text_input("✍️ اكتب وصف الأصل", placeholder="مثال: جهاز كمبيوتر محمول من نوع ديل")

# ========== معالجة البحث ==========
if user_input:
    with st.spinner('🔎 جاري البحث في قاعدة البيانات...'):
        try:
            # توليد تضمين الاستعلام
            inputs = tokenizer(user_input, return_tensors="pt", truncation=True, padding=True, max_length=32)
            with torch.no_grad():
                outputs = model(**inputs)
            query_embedding = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
            
            # حساب التشابه
            similarities = cosine_similarity([query_embedding], embeddings)[0]
            top_indices = similarities.argsort()[-5:][::-1]
            
            # عرض النتائج
            st.markdown("### 💡 أفضل 5 اقتراحات")
            for idx in top_indices:
                if similarities[idx] > 0.2:  # فلترة النتائج الضعيفة
                    with st.container():
                        st.markdown(f"""
                        <div class="result-card">
                            <h4>{asset_descriptions[idx]}</h4>
                            <p style="color: #2e86c1;">مستوى التشابه: {similarities[idx]:.2f}</p>
                            <p style="color: #27ae60;">الرمز: {df.iloc[idx]['Unique Asset Number in MoF system']}</p>
                        </div>
                        """, unsafe_allow_html=True)
            
            # رسم بياني للتشابه
            st.markdown("### 📊 توزيع التشابه")
            fig = pd.DataFrame({
                'التشابه': similarities,
                'الوصف': asset_descriptions
            }).plot(kind='hist', title='توزيع درجات التشابه').figure
            st.pyplot(fig)
            
        except Exception as e:
            st.error(f"⛔ حدث خطأ غير متوقع: {str(e)}")

# ========== قسم المساعدة ==========
with st.expander("ℹ️ تعليمات الاستخدام"):
    st.markdown("""
    **✨ ميزات النظام:**
    - بحث ذكي باستخدام أحدث نماذج الذكاء الاصطناعي
    - فلترة تلقائية للنتائج غير ذات الصلة
    - عرض مرئي للنتائج مع تفاصيل كاملة
    
    **🎯 نصائح البحث:**
    1. استخدم أوصافًا واضحة ومحددة
    2. تجنب الأخطاء الإملائية
    3. استخدم الكلمات المفتاحية المهمة
    """)
