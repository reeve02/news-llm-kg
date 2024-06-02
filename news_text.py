from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage
from langchain_core.prompts import HumanMessagePromptTemplate, ChatPromptTemplate
from langchain_openai import ChatOpenAI
from scrapping_news import get_news
import validators
import streamlit as st

OPENAI_API_KEY = st.secrets["openai_api_key"]

# Prompt untuk mendapatkan informasi dari berita dalam bentuk list
PROMPT_TEMPLATE1 = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content="""
            You are an assistant that helps to analyze news articles.
            Berikan semua entitas, relasi antar entitas, sentimen, kutipan dalam berita, unsur 5w1h, urutan kronologis kejadian, dan mereologi atau hubungan part-whole merupakan hal penting yang dibahas dan bersifat unik. 
            relasi antar entitas berisi relasi penting antara entitas dengan entitas lain atau relasi entitas dengan hal lain. 
            kutipan berisi hal yang dikatakan atau disebutkan secara langsung oleh sebuah individu. apabila tidak ada tidak perlu dituliskan.
            Berikut contoh berita dan hasil analisis berita yang diinginkan:
            contoh berita: Presiden Joko Widodo (Jokowi) dijadwalkan akan melantik Kepala Staf Angkatan Darat (KSAD) pada Rabu (29/11) di Istana Negara, Jakarta. Informasi itu dibenarkan oleh Ketua Komisi I DPR RI Meutya Hafid. "Ya betul (Jokowi lantik KSAD)," kata Meutya lewat pesan singkat, Selasa (28/11) malam. Namun demikian, Meutya belum memberitahu siapa perwira tinggi yang bakal mengisi kursi KSAD. Sebelumnya, salah satu yang disebut berpeluang besar menjadi KSAD adalah Panglima Komando Cadangan Strategis Angkatan Darat (Pangkostrad) Letjen Maruli Simanjuntak. Presiden Joko Widodo turut membenarkan Maruli merupakan satu dari sejumlah nama jenderal yang masuk dalam bursa KSAD. "Salah satu kandidat," kata Jokowi di Indonesia Arena, Jakarta, Sabtu (25/11). Posisi KSAD kosong setelah Jenderal Agus Subiyanto dilantik menjadi Panglima TNI. Agus sempat menjabat sebagai KSAD menggantikan Jenderal Dudung Abdurachman yang pensiun. Beberapa hari menjabat KSAD, Agus diusulkan Presiden Jokowi menjadi Panglima TNI. Ia baru dilantik pada pekan lalu
            contoh hasil analisis:

            Entitas:
            - Presiden Joko Widodo (Jokowi)
            - Ketua Komisi I DPR RI Meutya Hafid
            - Kepala Staf Angkatan Darat (KSAD)
            - Panglima Komando Cadangan Strategis Angkatan Darat (Pangkostrad) Letjen Maruli Simanjuntak
            - Jenderal Agus Subiyanto
            - Jenderal Dudung Abdurachman
            - Istana Negara, Jakarta

            Relasi Antarentitas:
            - Presiden Joko Widodo, melantik, KSAD
            - Meutya Hafid, mengkonfirmasi pelantikan, KSAD oleh Jokowi
            - Letjen Maruli Simanjuntak, berpeluang menjadi, KSAD
            - Jenderal Agus Subiyanto, diusulkan menjadi, Panglima TNI oleh Jokowi
            - Jenderal Dudung Abdurachman, digantikan oleh, Jenderal Agus Subiyanto sebagai KSAD

            Sentimen:
            - Positif terkait pelantikan KSAD baru oleh Presiden Jokowi

            Kutipan dalam Berita:
            - "Ya betul (Jokowi lantik KSAD)," - Meutya Hafid
            - "Salah satu kandidat," - Presiden Joko Widodo

            5W1H:
            - What: Pelantikan Kepala Staf Angkatan Darat (KSAD)
            - Who: Presiden Joko Widodo, Meutya Hafid, Letjen Maruli Simanjuntak, Jenderal Agus Subiyanto, Jenderal Dudung Abdurachman
            - When: Rabu, 29 November
            - Where: Istana Negara, Jakarta
            - Why: Pengisian posisi KSAD yang kosong
            - How: Pelantikan oleh Presiden Joko Widodo

            Urutan Kronologis Kejadian:
            - Posisi KSAD kosong setelah Jenderal Agus Subiyanto dilantik menjadi Panglima TNI.
            - Letjen Maruli Simanjuntak disebut sebagai salah satu kandidat KSAD oleh Presiden Jokowi.
            - Ketua Komisi I DPR RI Meutya Hafid mengkonfirmasi bahwa Presiden Jokowi akan melantik KSAD.
            - Pelantikan KSAD dijadwalkan pada Rabu, 29 November di Istana Negara, Jakarta.

            Hubungan Bagian-keseluruhan (Mereologi):
            - KSAD, bagian dari, Angkatan Darat TNI

            Ekstrak informasi untuk berita berikut:
            berita:
            """
        ),
        HumanMessagePromptTemplate.from_template("{context}"),
    ]
)

# Prompt untuk mendapatkan struktur markdown dari informasi berita yang telah dianalisis
PROMPT_TEMPLATE2 = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content = """
            You are an assistant that helps to create a structured markdown from analyzed news articles.
            Berdasarkan informasi dari berita berikut, tolong buatkan struktur data markdown yang mencakup triplets dari knowledge graph.
            Pastikan jawaban hanya berisi informasi dalam bentuk markdown.
            Struktur ini harus mencakup entitas, sentimen, dan kronologi peristiwa yang relevan.
            Sertakan juga kutipan yang relevan sebagai node quotes.

            Markdown Knowledge Graph harus terdiri dari nodes dan edges, seperti yang ditunjukkan pada contoh berikut:

            # Nodes

            ### Node ID: Presiden_Joko_Widodo
            **Label**: Presiden Joko Widodo (Jokowi)
            **Type**: Entity
            ---

            ### Node ID: Ketua_Komisi_I_DPR_RI_Meutya_Hafid
            **Label**: Ketua Komisi I DPR RI Meutya Hafid
            **Type**: Entity
            ---

            ### Node ID: KSAD
            **Label**: Kepala Staf Angkatan Darat (KSAD)
            **Type**: Entity
            ---

            ### Node ID: Panglima_Kostrad_Letjen_Maruli_Simanjuntak
            **Label**: Panglima Komando Cadangan Strategis Angkatan Darat (Pangkostrad) Letjen Maruli Simanjuntak
            **Type**: Entity
            ---

            ### Node ID: Jenderal_Agus_Subiyanto
            **Label**: Jenderal Agus Subiyanto
            **Type**: Entity
            ---

            ### Node ID: Jenderal_Dudung_Abdurachman
            **Label**: Jenderal Dudung Abdurachman
            **Type**: Entity
            ---

            ### Node ID: Istana_Negara_Jakarta
            **Label**: Istana Negara, Jakarta
            **Type**: Entity
            ---

            ### Node ID: Angkatan_Darat_TNI
            **Label**: Angkatan Darat TNI
            **Type**: Entity
            ---

            ### Node ID: Sentimen_Positif
            **Label**: Positif terkait pelantikan KSAD baru oleh Presiden Jokowi
            **Type**: Sentiment
            ---

            ### Node ID: Kutipan_Meutya_Hafid_1
            **Label**: "Ya betul (Jokowi lantik KSAD)," - Meutya Hafid
            **Type**: Quotes
            ---

            ### Node ID: Kutipan_Jokowi_1
            **Label**: "Salah satu kandidat," - Presiden Joko Widodo
            **Type**: Quotes
            ---

            ### Node ID: What
            **Label**: Pelantikan Kepala Staf Angkatan Darat (KSAD)
            **Type**: 5W1H
            ---

            ### Node ID: When
            **Label**: Rabu, 29 November
            **Type**: 5W1H
            ---

            ### Node ID: Where
            **Label**: Istana Negara, Jakarta
            **Type**: 5W1H
            ---

            ### Node ID: Why
            **Label**: Pengisian posisi KSAD yang kosong
            **Type**: 5W1H
            ---

            ### Node ID: How
            **Label**: Pelantikan dilakukan dengan upacara resmi oleh Presiden Joko Widodo di Istana Negara, Jakarta, dengan kehadiran pejabat tinggi negara
            **Type**: 5W1H
            ---

            ### Node ID: Who
            **Label**: Presiden Joko Widodo (Jokowi), Ketua Komisi I DPR RI Meutya Hafid, Kepala Staf Angkatan Darat (KSAD), Panglima Komando Cadangan Strategis Angkatan Darat (Pangkostrad) Letjen Maruli Simanjuntak, Jenderal Agus Subiyanto, Jenderal Dudung Abdurachman, Istana Negara, Jakarta
            **Type**: 5W1H
            ---

            ### Node ID: Kronologi1
            **Label**: Posisi KSAD kosong setelah Jenderal Agus Subiyanto dilantik menjadi Panglima TNI.
            **Type**: Chronology
            ---

            ### Node ID: Kronologi2
            **Label**: Letjen Maruli Simanjuntak disebut sebagai salah satu kandidat KSAD oleh Presiden Jokowi.
            **Type**: Chronology
            ---

            ### Node ID: Kronologi3
            **Label**: Ketua Komisi I DPR RI Meutya Hafid mengkonfirmasi bahwa Presiden Jokowi akan melantik KSAD.
            **Type**: Chronology
            ---

            ### Node ID: Kronologi4
            **Label**: Pelantikan KSAD dijadwalkan pada Rabu, 29 November di Istana Negara, Jakarta.
            **Type**: Chronology
            ---

            # Edges

            **Source**: What
            **Target**: KSAD
            **Label**: Berhubungan dengan
            ---

            **Source**: What
            **Target**: Presiden_Joko_Widodo
            **Label**: Berhubungan dengan
            ---

            **Source**: What
            **Target**: Ketua_Komisi_I_DPR_RI_Meutya_Hafid
            **Label**: Berhubungan dengan
            ---

            **Source**: What
            **Target**: Panglima_Kostrad_Letjen_Maruli_Simanjuntak
            **Label**: Berhubungan dengan
            ---

            **Source**: What
            **Target**: Jenderal_Agus_Subiyanto
            **Label**: Berhubungan dengan
            ---

            **Source**: What
            **Target**: Jenderal_Dudung_Abdurachman
            **Label**: Berhubungan dengan
            ---

            **Source**: What
            **Target**: When
            **Label**: Kapan
            ---

            **Source**: What
            **Target**: Where
            **Label**: Dimana
            ---

            **Source**: What
            **Target**: Why
            **Label**: Mengapa
            ---

            **Source**: What
            **Target**: How
            **Label**: Bagaimana
            ---

            **Source**: What
            **Target**: Who
            **Label**: Siapa
            ---

            **Source**: Who
            **Target**: Presiden_Joko_Widodo
            **Label**: Terkait
            ---

            **Source**: Who
            **Target**: Ketua_Komisi_I_DPR_RI_Meutya_Hafid
            **Label**: Terkait
            ---

            **Source**: Who
            **Target**: KSAD
            **Label**: Terkait
            ---

            **Source**: Who
            **Target**: Panglima_Kostrad_Letjen_Maruli_Simanjuntak
            **Label**: Terkait
            ---

            **Source**: Who
            **Target**: Jenderal_Agus_Subiyanto
            **Label**: Terkait
            ---

            **Source**: Who
            **Target**: Jenderal_Dudung_Abdurachman
            **Label**: Terkait
            ---

            **Source**: Who
            **Target**: Istana_Negara_Jakarta
            **Label**: Terkait
            ---

            **Source**: KSAD
            **Target**: Angkatan_Darat_TNI
            **Label**: bagian dari
            ---

            **Source**: Presiden_Joko_Widodo
            **Target**: KSAD
            **Label**: melantik
            ---

            **Source**: Ketua_Komisi_I_DPR_RI_Meutya_Hafid
            **Target**: KSAD
            **Label**: mengkonfirmasi pelantikan oleh Jokowi
            ---

            **Source**: Panglima_Kostrad_Letjen_Maruli_Simanjuntak
            **Target**: KSAD
            **Label**: berpeluang menjadi
            ---

            **Source**: Jenderal_Agus_Subiyanto
            **Target**: Panglima_TNI
            **Label**: diusulkan menjadi oleh Jokowi
            ---

            **Source**: Jenderal_Dudung_Abdurachman
            **Target**: Jenderal_Agus_Subiyanto
            **Label**: digantikan oleh sebagai KSAD
            ---

            **Source**: Sentimen_Positif
            **Target**: Presiden_Joko_Widodo
            **Label**: Sentimen
            ---

            **Source**: Kutipan_Meutya_Hafid_1
            **Target**: Ketua_Komisi_I_DPR_RI_Meutya_Hafid
            **Label**: Pernyataan
            ---

            **Source**: Kutipan_Jokowi_1
            **Target**: Presiden_Joko_Widodo
            **Label**: Pernyataan
            ---

            **Source**: How
            **Target**: Kronologi1
            **Label**: Dimulai dengan
            ---

            **Source**: Kronologi1
            **Target**: Kronologi2
            **Label**: Dilanjutkan dengan
            ---

            **Source**: Kronologi2
            **Target**: Kronologi3
            **Label**: Dilanjutkan dengan
            ---

            **Source**: Kronologi3
            **Target**: Kronologi4
            **Label**: Berakhir dengan
            ---

            Berikanlah struktur markdown yang mencakup nodes dan edges. Nodes harus mencakup:
            - Entity: individu, organisasi, atau lokasi yang penting dalam berita.
            - Sentiment: sentimen terhadap peristiwa atau terhadap entitas tertentu.
            - Quotes: pernyataan langsung dari narasumber yang relevan.
            - Chronology: Urutan terjadinya peristiwa pada berita

            Nodes hanya memiliki 4 tipe yaitu Entity, Sentiment, Quotes, dan Chronology.
            Pastikan bahwa setiap entitas terhubung ke nodes utama dan tidak ada nodes yang terpisah.
            Pastikan bahwa semua node yang disebutkan di dalam edges sudah didefinisikan di bagian nodes sebagai ID node.
            Gunakan Bahasa Indonesia.

            Berikut merupakan informasi yang perlu dijadikan struktur markdown:
            """
        ),
        HumanMessagePromptTemplate.from_template("{context}")
    ]
)

# Fungsi untuk memproses teks berita
def process_news(news_text):
    prompt_template1 = PROMPT_TEMPLATE1.format(context=news_text)
    
    # Inisiialisasi chatbot OpenAI
    model = ChatOpenAI(api_key=OPENAI_API_KEY, model="gpt-4o")

    # Melakukan pemanggilan berantai untuk mendapatkan hasil analisis berita dan struktur markdown
    response_message1 = model.invoke(prompt_template1)
    response_text1 = response_message1.content.strip()

    prompt_template2 = PROMPT_TEMPLATE2.format(context=response_text1)
    response_message2 = model.invoke(prompt_template2)
    response_text2 = response_message2.content.strip()
    
    print("the markdown: " + response_text2)

    return response_text1, response_text2

# Fungsi untuk memproses link berita
def process_link(news_link):
    if not validators.url(news_link):
        return "Error: Invalid URL format."
    result = get_news(news_link)
    if result is None or 'content' not in result or not result['content']:
        return "Error: Could not get the news content from the link."
    else:
        return process_news(result['content'])