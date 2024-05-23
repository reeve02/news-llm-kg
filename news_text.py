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
            Berikan semua entitas, relasi antar entitas, sentimen, kutipan dalam berita, unsur 5w1h, urutan kronologis kejadian, dan kategori usia merupakan hal penting yang dibahas dan bersifat unik. 
            relasi antar entitas berisi relasi penting antara entitas dengan entitas lain atau relasi entitas dengan hal lain. 
            kutipan berisi hal yang dikatakan atau disebutkan secara langsung oleh sebuah individu. apabila tidak ada tidak perlu dituliskan.
            Berita termasuk kategori dewasa jika mengandung unsur kekerasan, konten seksual, penggunaan obat terlarang, dan bahasa kasar. Jika tidak mengandung unsur tersebut, berita dapat dikategorikan sebagai "Semua umur"
            cukup berikan informasi yang penting dan memudahkan pengguna dalam memahami berita.
            Berikut contoh berita dan hasil analisis berita yang diinginkan:
            contoh berita: Pihak Universitas Gadjah Mada (UGM) buka suara soal kabar penolakan kehadiran capres nomor urut satu Anies Baswedan oleh pihak yang mengatasnamakan rektorat untuk menghadiri sebuah acara diskusi sebagai narasumber. Sekretaris UGM Andi Sandi Antonius mengatakan pihaknya saat ini masih melakukan penelusuran lebih lanjut. Pasalnya, Andi juga belum mengetahui pihak yang diklaim panitia mengaku sebagai 'rektorat tersebut. Ia mengacu pada tangkapan layar percakapan WhatsApp dengan nama kontak 'rektorat' yang viral di media sosial. "Menjadi aneh saya dapat kiriman katanya ada orang namanya Pak Wija pakai akun nama 'rektorat', sebenarnya saya mau tanya itu siapa," kata Andi saat dihubungi. "Menurut kami, yang sangat memojokkan UGM adalah dikatakan rektorat akan menolak. Nah siapa orang di rektorat itu saya sudah tanya ke bu rektor, saya tanya ke teman-teman wakil rektor ini tidak ada yang memberikan statement ini," sambungnya. Oleh karenanya, pihaknya belum bisa memberikan tanggapan lebih jauh mengenai kabar penolakan kedatangan Anies serta pembatalan acara ini. "Karena kalau dilaksanakan UGM kami kan sudah punya SOP biar bagaimanapun kita harus memisahkan ini dalam ranah kampanye atau tidak. Kalau ranah kampanye kita sudah punya SOP kami yang harus mengundang. UGM yang harus mengundang," tegasnya. Andi sendiri menekankan kampusnya sangat 'welcome' dengan kedatangan Anies, apalagi sebagai narasumber acara akademik. Dia menyebut UGM adalah rumah juga buat Anies yang merupakan alumnus universitas tersebut. Sebelumnya panitia acara diskusi yang bertajuk 'Indonesian Future Stadium Generale' itu mengklaim tak mendapatkan rekomendasi atau izin dari rektorat kampus untuk mengundang Anies sebagai narasumber. Panitia mengklaim rektorat mengancam akan membubarkan acara yang digelar di Auditorium MM UGM itu apabila mereka tetap mengundang capres dari Koalisi Perubahan tersebut. Acara diskusi yang digelar pada Jumat (17/11) mulai pukul 13.00 WIB itu diselenggarakan oleh lembaga swadaya masyarakat (LSM) Bersama Indonesia. Anies diundang dalam kapasitasnya sebagai Gubernur DKI Jakarta 2017-2022 membahas topik 'Finding Justice Development for the Future of Indonesia: Promoting Jakarta 'Kota Kolaborasi' as a Pioneer of Global Sharing City'. Public Affairs Bersama Indonesia Muhammad Khalid mengatakan nama Thomas Lembong diajukan sebagai pengganti setelah panitia tidak mendapatkan rekomendasi dari rektorat untuk menghadirkan Anies. "Ada satu rekomendasi dari pengelola tempat yang tentu saja kampus UGM, karena kita sifatnya menyewa tempat di sini. Rekomendasinya yaitu bahwa tidak menyarankan kehadiran tokoh ini, bapak Anies Baswedan karena dianggapnya melekat dengan unsur unsur politis di fase-fase saat ini," kata Khalid ditemui di Auditorium MM UGM. Berdasarkan pantauan di lokasi, kehadiran Anies sebagai narasumber digantikan Thomas Trikasih Lembong selaku menteri perdagangan 2015-2016 dan Kepala Badan Koordinasi Penanaman Modal (BKPM) 2016-2019. Thomas yang kini juga ditunjuk menjadi salah satu co-captain dalam Tim Nasional Pemenangan Anies Baswedan-Muhaimin Iskandar (Timnas AMIN) untuk Pilpres 2024, hadir secara daring dalam acara tersebut. Khalid menjelaskan, acara ini sudah terencana sejak dua pekan lalu dan mencantumkan nama Anies sebagai salah satu narasumbernya. Saat itu pihaknya berkoordinasi dengan pihak prodi MM FEB UGM selaku pengelola tempat dan tidak ada catatan apapun terkait acara. Khalid mengklaim kala itu semua sudah 'deal'. Khalid menjelaskan selebaran acara disebar melalui media sosial pada H-2. Namun, sehari berselang atau Kamis (16/11) petang, pengelola lokasi acara mengirimkan pesan terusan WhatsApp dari rektorat kepada panitia. Intinya agar Anies tidak dihadirkan sebagai narasumber. "Di situ ada redaksi (kalimat) bahwa apabila tetap memaksakan seperti itu akan ada aparat keamanan yang menertibkan acara ini atau dalam bahasa sederhananya dibubarkan," klaim Khalid. Khalid pun menunjukkan percakapan WhatsApp antara dirinya dengan seseorang bernama kontak 'rektorat' yang ia panggil dengan nama 'Pak Wija'. Isi percakapannya adalah meminta Khalid untuk memastikan kedatangan Anies. Selain itu ada anjuran rektor agar acara dibatalkan jika Anies tetap didatangkan. Kata dia, tangkapan layar percakapan ini sudah viral di media sosial X (Twitter). Khalid mengaku sudah menjelaskan konsep acara yang digelar pihaknya adalah yakni agar generasi muda melek dan terlibat dalam suatu proses kebijakan publik yang berorientasi pada keadilan sosial. Sehingga, tema sharing city dimaksudkan mendorong kota pembangunan yang berkeadilan. "Jadi bagaimana kita mengangkat praktik baik di Jakarta pada masa Anies Baswedan dulu adalah salah satu ide jangka panjang di masa depan yang desainnya itu akan didiskusikan dan diafirmasi oleh berbagai background juga. Ada praktisi. Jadi tujuan utamanya tentu saja itu, kehadiran pak Anies sebagai tokoh mantan gubernur, dulu yang memberikan legacy itu di Jakarta adalah satu nilai tambah," imbuhnya. Khalid mengatakan, pihaknya sudah berargumen bahwa acaranya murni diskusi akademik dan bukan wadah kampanye peserta Pilpres 2024. Namun, demi keberlangsungan acara pihaknya akhirnya mengalah. Poster acara yang rencananya dipasang di simpang empat MM FEB UGM ujung-ujungnya urung dipasang. "Dengan pertimbangan seperti itu, kami menganggap demi kebaikan bersama kita juga memilih menggantikan beliau dengan tadi bapak Thomas Trikasih Lembong," ucapnya.
            contoh hasil analisis:

            Entitas:
            - Universitas Gadjah Mada (UGM)
            - Anies Baswedan
            - Sekretaris UGM Andi Sandi Antonius
            - Panitia 'Indonesian Future Stadium Generale'
            - Muhammad Khalid (Public Affairs Bersama Indonesia)
            - Thomas Trikasih Lembong

            Relasi Antarentitas:
            - Anies Baswedan, ditolak hadir sebagai narasumber, oleh entitas yang mengaku 'rektorat' UGM
            - UGM, diklaim menolak, Anies Baswedan
            - Andi Sandi Antonius, mencari informasi tentang, 'rektorat'
            - UGM, melakukan penelusuran, atas klaim penolakan Anies
            - LSM Bersama Indonesia, menggantikan Anies dengan, Thomas Trikasih Lembong sebagai narasumber

            Sentimen:
            - Negatif mengenai Kekeliruan dan penyesatan informasi terkait klaim penolakan Anies

            Kutipan dalam Berita:
            - ""Menjadi aneh saya dapat kiriman katanya ada orang namanya Pak Wija pakai akun nama 'rektorat', sebenarnya saya mau tanya itu siapa,"" - Andi Sandi Antonius
            - ""Nah siapa orang di rektorat itu saya sudah tanya ke bu rektor, saya tanya ke teman-teman wakil rektor ini tidak ada yang memberikan statement ini,"" - Andi Sandi Antonius
            - ""Kalau ranah kampanye kita sudah punya SOP kami yang harus mengundang. UGM yang harus mengundang,"" - Andi Sandi Antonius
            - ""Ada satu rekomendasi dari pengelola tempat yang tentu saja kampus UGM, karena kita sifatnya menyewa tempat di sini. Rekomendasinya yaitu bahwa tidak menyarankan kehadiran tokoh ini, bapak Anies Baswedan karena dianggapnya melekat dengan unsur unsur politis di fase-fase saat ini,"" - Muhammad Khalid
            - ""Di situ ada redaksi (kalimat) bahwa apabila tetap memaksakan seperti itu akan ada aparat keamanan yang menertibkan acara ini atau dalam bahasa sederhananya dibubarkan,"" - Muhammad Khalid
            - ""Jadi bagaimana kita mengangkat praktik baik di Jakarta pada masa Anies Baswedan dulu adalah salah satu ide jangka panjang di masa depan yang desainnya itu akan didiskusikan dan diafirmasi oleh berbagai background juga. Ada praktisi,"" - Muhammad Khalid

            5W1H:
            - What: Penolakan Anies Baswedan hadir diskusi
            - Who: UGM, Anies Baswedan, Andi Sandi Antonius, Muhammad Khalid, Thomas Trikasih Lembong
            - When: Jumat, 17 November, mulai pukul 13.00 WIB
            - Where: Auditorium MM UGM
            - Why: Kekhawatiran atas unsur politis kehadiran Anies
            - How: Penggantian narasumber, penyebaran informasi melalui WhatsApp

            Urutan Kronologis Kejadian:
            - Panitia merencanakan acara dan mengundang Anies sebagai narasumber.
            - Panitia mendapat pesan dari 'rektorat' yang menyarankan agar Anies tidak dihadirkan.
            - UGM, melalui Andi Sandi Antonius, menyatakan ketidakpastian tentang siapa di rektorat yang mengeluarkan penolakan.
            - Muhammad Khalid mengumumkan Thomas Lembong sebagai pengganti Anies.

            Kategori Usia:
            - Semua Umur, Berita tidak mengandung kekerasan atau yang melanggar hukum

            Berikut berita yang perlu dianalisis:
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

            ### Node ID: Maurits_Mantiri
            **Label**: Wali Kota Bitung (Maurits Mantiri)
            **Type**: Entity
            ---

            ### Node ID: Pemerintah_Kota_Bitung
            **Label**: Pemerintah Kota Bitung
            **Type**: Entity
            ---

            ### Node ID: Ormas
            **Label**: Ormas
            **Type**: Entity
            ---

            ### Node ID: Massa_Pro_Palestina
            **Label**: Massa pro Palestina
            **Type**: Entity
            ---

            ### Node ID: Bentrokan
            **Label**: Bentrokan
            **Type**: Entity
            ---

            ### Node ID: Kapolda_Sulut_Irjen_Setyo_Budiyanto
            **Label**: Kapolda Sulawesi Utara (Irjen Setyo Budiyanto)
            **Type**: Entity
            ---

            ### Node ID: TNI_Polri
            **Label**: TNI/Polri
            **Type**: Entity
            ---

            ### Node ID: Sentimen_Positif
            **Label**: Positif: upaya mendamaikan dan mengembalikan ketertiban yang terhubung massa pro palestina
            **Type**: Sentiment
            ---

            ### Node ID: Kutipan_Kondusif
            **Label**: Saat ini, pusat Kota Bitung dalam keadaan kondusif dan aman terkendali,
            **Type**: Quotes
            ---

            ### Node ID: What
            **Label**: Bentrokan antara ormas dengan massa pro Palestina
            **Type**: 5W1H
            ---

            ### Node ID: Who
            **Label**: Yang Terlibat
            **Type**: 5W1H
            ---

            ### Node ID: When
            **Label**: Sabtu 25 November
            **Type**: 5W1H
            ---

            ### Node ID: Where
            **Label**: Kota Bitung, Sulawesi Utara
            **Type**: 5W1H
            ---

            ### Node ID: Why
            **Label**: Perbedaan pendapat dan partisipasi dalam aksi
            **Type**: 5W1H
            ---

            ### Node ID: How
            **Label**: Aparat gabungan TNI-Polri meredam situasi
            **Type**: 5W1H
            ---

            ### Node ID: Kronologi1
            **Label**: Terjadi bentrokan antara dua kelompok ormas
            **Type**: Chronology
            ---

            ### Node ID: Kronologi2
            **Label**: TNI/Polri turun tangan meredam kericuhan
            **Type**: Chronology
            ---

            ### Node ID: Kronologi3
            **Label**: Wali Kota Bitung menyatakan situasi sudah kondusif
            **Type**: Chronology
            ---

            # Edges

            **Source**: Ormas
            **Target**: Massa_Pro_Palestina
            **Label**: terlibat dalam bentrokan dengan
            ---

            **Source**: Pemerintah_Kota_Bitung
            **Target**: TNI_Polri
            **Label**: bekerja sama dengan
            ---

            **Source**: Maurits_Mantiri
            **Target**: Kota_Bitung
            **Label**: menyatakan kondusif
            ---

            **Source**: Pemerintah_Kota_Bitung
            **Target**: Sentimen_Positif
            **Label**: Sentimen
            ---

            **Source**: Maurits_Mantiri
            **Target**: Kutipan_Kondusif
            **Label**: menyatakan
            ---

            **Source**: Bentrokan
            **Target**: What
            **Label**: Apa Yang Terjadi
            ---

            **Source**: Who
            **Target**: Ormas
            **Label**: Siapa Yang Terlibat
            ---

            **Source**: Who
            **Target**: Massa_Pro_Palestina
            **Label**: Siapa Yang Terlibat
            ---

            **Source**: Who
            **Target**: TNI_Polri
            **Label**: Siapa Yang Terlibat
            ---

            **Source**: Who
            **Target**: Pemerintah_Kota_Bitung
            **Label**: Siapa Yang Terlibat
            ---

            **Source**: Bentrokan
            **Target**: When
            **Label**: Kapan
            ---

            **Source**: Bentrokan
            **Target**: Where
            **Label**: Dimana
            ---

            **Source**: Bentrokan
            **Target**: Why
            **Label**: Mengapa
            ---

            **Source**: Bentrokan
            **Target**: How
            **Label**: Bagaimana terjadinya
            ---

            **Source**: Bentrokan
            **Target**: Kronologi1
            **Label**: Dimulai dengan
            ---

            **Source**: Kronologi1
            **Target**: Kronologi2
            **Label**: Dilanjutkan dengan
            ---

            **Source**: Kronologi2
            **Target**: Kronologi3
            **Label**: Berakhir dengan
            ---

            **Source**: Bentrokan
            **Target**: Pemerintah_Kota_Bitung
            **Label**: Merupakan bagian dari tantangan keamanan bagi
            ---

            **Source**: Maurits_Mantiri
            **Target**: Pemerintah_Kota_Bitung
            **Label**: Merupakan bagian dari
            ---

            **Source**: Kapolda_Sulut_Irjen_Setyo_Budiyanto
            **Target**: TNI_Polri
            **Label**: Merupakan bagian dari
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