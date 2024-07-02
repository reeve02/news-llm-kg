from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage
from langchain_core.prompts import HumanMessagePromptTemplate, ChatPromptTemplate
from langchain_openai import ChatOpenAI
import streamlit as st

OPENAI_API_KEY = st.secrets["openai_api_key"]

# Prompt untuk mengubah triplet markdown menjadi RDF turtle
PROMPT_TEMPLATE1 = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content="""
            You are an assistant that helps to convert Markdown that contains Knowledge Graph Triples into RDF Turtle format.
            
            Ubah setiap triplet KG menjadi pernyataan RDF.
            Pastikan jawaban hanya berisi informasi dalam format RDF Turtle.
            Ketika menghasilkan teks untuk RDF, hindari penggunaan karakter yang membutuhkan escape character, seperti kutip tunggal (').
            Penggunaan tanda petik dua (") pada kutipan dapat mengikuti contoh yang diberikan.
            Tidak perlu menggunakan ```turtle pada awal teks dan ``` pada akhir teks.
                        
            Berikut contoh triplet dalam markdown dan hasil konversi yang diinginkan dalam format RDF turtle:
            Contoh triplet dalam markdown:
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
            **Label**: Di mana
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

            Contoh hasil konversi dalam format RDF turtle:

            @prefix :      <http://example.org/berita-indonesia/> .
            @prefix rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
            @prefix rdfs:  <http://www.w3.org/2000/01/rdf-schema#> .
            @prefix xsd:   <http://www.w3.org/2001/XMLSchema#> .

            # Triples
            :Pelantikan_KSAD :berhubunganDengan :KSAD, :Presiden_Joko_Widodo, :Ketua_Komisi_I_DPR_RI_Meutya_Hafid, 
                                                :Panglima_Kostrad_Letjen_Maruli_Simanjuntak, :Jenderal_Agus_Subiyanto, 
                                                :Jenderal_Dudung_Abdurachman .
            :Pelantikan_KSAD :kapan "2023-11-29"^^xsd:date .
            :Pelantikan_KSAD :di mana :Istana_Negara_Jakarta .
            :Pelantikan_KSAD :mengapa "Pengisian posisi KSAD yang kosong" .
            :Pelantikan_KSAD :bagaimana "Pelantikan dilakukan dengan upacara resmi oleh Presiden Joko Widodo di Istana Negara, Jakarta, dengan kehadiran pejabat tinggi negara" .
            :Pelantikan_KSAD :siapa :Presiden_Joko_Widodo, :Ketua_Komisi_I_DPR_RI_Meutya_Hafid, :KSAD, 
                                    :Panglima_Kostrad_Letjen_Maruli_Simanjuntak, :Jenderal_Agus_Subiyanto, 
                                    :Jenderal_Dudung_Abdurachman .

            :KSAD :bagianDari :Angkatan_Darat_TNI .
            :Presiden_Joko_Widodo :melantik :KSAD .
            :Ketua_Komisi_I_DPR_RI_Meutya_Hafid :mengkonfirmasiPelantikan :KSAD .
            :Panglima_Kostrad_Letjen_Maruli_Simanjuntak :berpeluangMenjadi :KSAD .
            :Jenderal_Agus_Subiyanto :diusulkanMenjadi :Panglima_TNI .
            :Jenderal_Agus_Subiyanto :digantikanOleh :Jenderal_Dudung_Abdurachman .

            :Presiden_Joko_Widodo :memilikiSentimen "Positif terkait pelantikan KSAD baru" .
            :Ketua_Komisi_I_DPR_RI_Meutya_Hafid :membuatPernyataan "Ya betul (Jokowi lantik KSAD)" .
            :Presiden_Joko_Widodo :membuatPernyataan "Salah satu kandidat" .

            :Kronologi1 rdf:type :Kronologi ;
                rdfs:label "Posisi KSAD kosong setelah Jenderal Agus Subiyanto dilantik menjadi Panglima TNI" .
            :Kronologi2 rdf:type :Kronologi ;
                rdfs:label "Letjen Maruli Simanjuntak disebut sebagai salah satu kandidat KSAD oleh Presiden Jokowi" .
            :Kronologi3 rdf:type :Kronologi ;
                rdfs:label "Ketua Komisi I DPR RI Meutya Hafid mengkonfirmasi bahwa Presiden Jokowi akan melantik KSAD" .
            :Kronologi4 rdf:type :Kronologi ;
                rdfs:label "Pelantikan KSAD dijadwalkan pada Rabu, 29 November di Istana Negara, Jakarta" .

            :Pelantikan_KSAD :dimulaiBerakhirDengan :Kronologi1 .
            :Kronologi1 :dilanjutkanDengan :Kronologi2 .
            :Kronologi2 :dilanjutkanDengan :Kronologi3 .
            :Kronologi3 :berakhirDengan :Kronologi4 .

            Berikut merupakan markdown yang perlu dijadikan RDF turtle:
            """
        ),
        HumanMessagePromptTemplate.from_template("{context}"),
    ]
)

# Fungsi untuk mengubah hasil markdown menjadi RDF turtle
def md_rdf(md_input):
    prompt_template1 = PROMPT_TEMPLATE1.format(context=md_input)
    
    # Inisiialisasi chatbot OpenAI
    model = ChatOpenAI(api_key=OPENAI_API_KEY, model="gpt-4o")

    # Melakukan pemanggilan LLM untuk mendapatkan format menjadi RDF turtle
    response_message = model.invoke(prompt_template1)
    response_text = response_message.content.strip()

    return response_text
