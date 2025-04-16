
import streamlit as st
import pandas as pd
import torch
from sklearn.metrics.pairwise import cosine_similarity
from transformers import AutoTokenizer, AutoModel

st.set_page_config(page_title="اقتراحات BERT الذكية", layout="wide")
st.title("🤖 نظام اقتراح وصف الأصل باستخدام BERT")

# تحميل البيانات
df = pd.read_excel("assetv4.xlsx", header=1)
df.columns = df.columns.str.strip()
asset_descriptions = df["Asset Description For Maintenance Purpose"].dropna().astype(str).unique().tolist()

# تحميل BERT العربي
@st.cache_resource
def load_model():
    tokenizer = AutoTokenizer.from_pretrained("asafaya/bert-base-arabic")
    model = AutoModel.from_pretrained("asafaya/bert-base-arabic")
    return tokenizer, model

tokenizer, model = load_model()

# دالة لاستخراج التضمين من BERT
def get_embedding(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=32)
    with torch.no_grad():
        outputs = model(**inputs)
    embedding = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
    return embedding

# تجهيز التضمينات مسبقاً
@st.cache_resource
def embed_all_descriptions():
    embeddings = []
    for desc in asset_descriptions:
        try:
            emb = get_embedding(desc)
            embeddings.append(emb)
        except:
            embeddings.append([0]*768)
    return embeddings

description_embeddings = embed_all_descriptions()

# واجهة المستخدم
user_input = st.text_input("✍️ اكتب وصف الأصل")

if user_input:
    query_vec = get_embedding(user_input)
    similarities = cosine_similarity([query_vec], description_embeddings)[0]
    top_indices = similarities.argsort()[-3:][::-1]
    st.markdown("### 💡 اقتراحات ذكية من BERT:")
    for i in top_indices:
        st.markdown(f"- {asset_descriptions[i]} (تشابه: {similarities[i]:.2f})")
