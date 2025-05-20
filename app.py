# import streamlit as st
# import requests
# import pandas as pd
# from collections import Counter

# API_KEY = "d385bda21f564c88a4351d7b72b00651"

# st.set_page_config(page_title="Berita & Statistik Golf", page_icon="🏌️")

# st.title("🏌️ Aplikasi Berita & Statistik Golf")

# tab1, tab2 = st.tabs(["📰 Berita Golf", "📊 Statistik Kata Kunci"])

# # ---------- TAB 1: Berita Golf ----------
# with tab1:
#     st.header("📰 Cari Berita Golf")
#     st.write("Temukan berita terbaru seputar dunia golf.")

#     query = st.text_input("Masukkan kata kunci berita golf (contoh: Tiger Woods, PGA, Masters)")

#     if query:
#         url = "https://newsapi.org/v2/everything"
#         params = {
#             "q": query,
#             "language": "en",
#             "pageSize": 10,
#             "apiKey": API_KEY
#         }

#         response = requests.get(url, params=params)
#         data = response.json()

#         if response.status_code == 200 and data.get("articles"):
#             st.success(f"Ditemukan {len(data['articles'])} artikel:")

#             for article in data["articles"]:
#                 with st.expander(article.get("title", "Judul tidak tersedia")):
#                     st.write(f"📅 {article.get('publishedAt', '')[:10]}")
#                     st.write(article.get("description", "Deskripsi tidak tersedia."))
#                     if article.get("urlToImage"):
#                         st.image(article["urlToImage"], width=300)
#                     if article.get("url"):
#                         st.markdown(f"[Baca Selengkapnya]({article['url']})")
#         else:
#             st.warning("Tidak ada berita ditemukan atau terjadi kesalahan.")

# # ---------- TAB 2: Statistik Kata Kunci dari Judul Berita ----------
# with tab2:
#     st.header("📊 Analisis Kata Populer dalam Judul Berita")

#     query2 = st.text_input("Masukkan kata kunci utama (misalnya 'golf', 'Rory McIlroy')", key="query2")

#     if query2:
#         url = "https://newsapi.org/v2/everything"
#         params = {
#             "q": query2,
#             "language": "en",
#             "pageSize": 50,
#             "apiKey": API_KEY
#         }

#         response = requests.get(url, params=params)
#         data = response.json()

#         if response.status_code == 200 and data.get("articles"):
#             word_counter = Counter()
#             for article in data["articles"]:
#                 title = article.get("title", "")
#                 words = title.lower().split()
#                 for word in words:
#                     if len(word) > 3:  # hindari kata pendek seperti "the", "and"
#                         word_counter[word] += 1

#             top_words = word_counter.most_common(10)
#             df = pd.DataFrame(top_words, columns=["Kata", "Jumlah Muncul"])

#             st.bar_chart(df.set_index("Kata"))
#             st.dataframe(df)
#         else:
#             st.warning("Gagal memuat data berita.")

import streamlit as st
import requests
import pandas as pd
from collections import Counter
from pymongo import MongoClient

# Koneksi ke MongoDB Atlas
client = MongoClient("mongodb+srv://dappaa:dapa123@capstone6.ohrqo4p.mongodb.net/?retryWrites=true&w=majority&appName=capstone6")
db = client['capstone6']
collection_article = db['article']
collection_lokasi = db['lokasi']
collection_tutorial = db['tutorial']

# API key untuk NewsAPI
API_KEY = "d385bda21f564c88a4351d7b72b00651"

# Konfigurasi halaman
st.set_page_config(page_title="Berita & Statistik Golf", page_icon="🏌️")

st.title("🏌️ Aplikasi Berita & Statistik Golf")

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📰 Berita Golf", 
    "📊 Statistik Kata Kunci", 
    "📋 Hasil Scraping Artikel", 
    "📍 Hasil Scraping Lokasi (YouTube)", 
    "🎯 Hasil Scraping Tutorial (YouTube)"
])

# ---------- TAB 1: Berita Golf ----------
with tab1:
    st.header("📰 Cari Berita Golf")
    query = st.text_input("Masukkan kata kunci berita golf (contoh: Tiger Woods, PGA, Masters)")

    if query:
        url = "https://newsapi.org/v2/everything"
        params = {
            "q": query,
            "language": "en",
            "pageSize": 10,
            "apiKey": API_KEY
        }

        response = requests.get(url, params=params)
        data = response.json()

        if response.status_code == 200 and data.get("articles"):
            st.success(f"Ditemukan {len(data['articles'])} artikel:")
            for article in data["articles"]:
                with st.expander(article.get("title", "Judul tidak tersedia")):
                    st.write(f"📅 {article.get('publishedAt', '')[:10]}")
                    st.write(article.get("description", "Deskripsi tidak tersedia."))
                    if article.get("urlToImage"):
                        st.image(article["urlToImage"], width=300)
                    if article.get("url"):
                        st.markdown(f"[Baca Selengkapnya]({article['url']})")
        else:
            st.warning("Tidak ada berita ditemukan atau terjadi kesalahan.")

# ---------- TAB 2: Statistik Kata Kunci ----------
with tab2:
    st.header("📊 Analisis Kata Populer dalam Judul Berita")

    query2 = st.text_input("Masukkan kata kunci utama (misalnya 'golf', 'Rory McIlroy')", key="query2")

    if query2:
        url = "https://newsapi.org/v2/everything"
        params = {
            "q": query2,
            "language": "en",
            "pageSize": 50,
            "apiKey": API_KEY
        }

        response = requests.get(url, params=params)
        data = response.json()

        if response.status_code == 200 and data.get("articles"):
            word_counter = Counter()
            for article in data["articles"]:
                title = article.get("title", "")
                words = title.lower().split()
                for word in words:
                    if len(word) > 3:
                        word_counter[word] += 1

            top_words = word_counter.most_common(10)
            df = pd.DataFrame(top_words, columns=["Kata", "Jumlah Muncul"])

            st.bar_chart(df.set_index("Kata"))
            st.dataframe(df)
        else:
            st.warning("Gagal memuat data berita.")

# ---------- TAB 3: Scraping Artikel ----------
with tab3:
    st.header("📋 Judul Artikel dari Scraping Web")
    articles = list(collection_article.find({}, {"_id": 0}))
    
    if articles:
        df = pd.DataFrame(articles)
        st.write(f"Ditemukan {len(df)} artikel.")
        st.dataframe(df)

        word_counter = Counter()
        for row in df['judul']:
            for word in row.lower().split():
                if len(word) > 3:
                    word_counter[word] += 1
        top_words = word_counter.most_common(10)
        df_chart = pd.DataFrame(top_words, columns=["Kata", "Jumlah"])
        st.bar_chart(df_chart.set_index("Kata"))
    else:
        st.warning("Tidak ada data artikel.")

# ---------- TAB 4: Scraping Lokasi YouTube ----------
with tab4:
    st.header("📍 Video Lokasi Lapangan Golf")
    videos = list(collection_lokasi.find({}, {"_id": 0}))
    
    if videos:
        df = pd.DataFrame(videos)
        st.write(f"Ditemukan {len(df)} video lokasi.")
        st.dataframe(df[['title', 'channel', 'link', 'scraped_at']])

        word_counter = Counter()
        for title in df['title']:
            for word in title.lower().split():
                if len(word) > 3:
                    word_counter[word] += 1
        top_words = word_counter.most_common(10)
        df_chart = pd.DataFrame(top_words, columns=["Kata", "Jumlah"])
        st.bar_chart(df_chart.set_index("Kata"))
    else:
        st.warning("Tidak ada data video lokasi.")

# ---------- TAB 5: Scraping Tutorial YouTube ----------
with tab5:
    st.header("🎯 Video Tutorial Golf")
    tutorials = list(collection_tutorial.find({}, {"_id": 0}))
    
    if tutorials:
        df = pd.DataFrame(tutorials)
        st.write(f"Ditemukan {len(df)} video tutorial.")
        st.dataframe(df[['title', 'channel', 'link', 'scraped_at']])

        word_counter = Counter()
        for title in df['title']:
            for word in title.lower().split():
                if len(word) > 3:
                    word_counter[word] += 1
        top_words = word_counter.most_common(10)
        df_chart = pd.DataFrame(top_words, columns=["Kata", "Jumlah"])
        st.bar_chart(df_chart.set_index("Kata"))
    else:
        st.warning("Tidak ada data video tutorial.")
