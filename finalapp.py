import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
from md_parser import parse_markdown
from news_text import process_news, process_link
from PIL import Image

im = Image.open("kg-llm.ico")

st.set_page_config(
    page_title="news-llm-kg",
    page_icon=im,
    layout="wide",
)

# memuat CSS untuk styling
with open("styles.css", "r") as f:
    styles = f.read()
st.markdown(f"<style>{styles}</style>", unsafe_allow_html=True)

st.markdown("Masukkan input teks atau link berita pada area sidebar", help="Sidebar pada perangkat mobile dapat dibuka dengan mengklik tanda panah kanan \(>\) di pojok kiri atas halaman")

st.sidebar.title("👩‍💻Knowledge Graph Berita")
st.sidebar.markdown("Pastikan link berita termasuk dalam daftar link yang didukung", help="List berita yang didukung:\n- CNBC Indonesia\n- Liputan6\n- Narasi.tv\n- Antara News\n- CNN Indonesia\n- Detik.com\n- Kompas")

input_option = st.sidebar.selectbox(
    "Pilih opsi input berita:",
    ["Masukkan teks berita", "Masukkan link berita"],
    key="input_option_selectbox"
)

# Input data berdasarkan opsi yang dipilih
input_data = None
if input_option == "Masukkan teks berita":
    input_data = st.sidebar.text_area("Masukkan teks berita:", key="text_input")
elif input_option == "Masukkan link berita":
    input_data = st.sidebar.text_area("Masukkan link berita:", key="link_input")


def load_data(input_data):
    if input_option == "Masukkan teks berita":
        list_result, md_result  = process_news(input_data)
        try:
            parsed_data = parse_markdown(md_result)
        except Exception as e:
            st.error(f"Error parsing data: {e}")
            return None, None
        return list_result, parsed_data
    elif input_option == "Masukkan link berita":
        try:
            list_result, md_result = process_link(input_data)
            try:
                parsed_data = parse_markdown(md_result)
            except Exception as e:
                st.error(f"Error parsing data: {e}")
                return None, None
            return list_result, parsed_data
        except TypeError:
            st.error("Error: Tidak dapat memproses link berita.")
            return None, None

submit_button = st.sidebar.button("Submit Berita")

if submit_button and input_data:
    try:
        list_result, data = load_data(input_data)
        if data is None:
            st.error("Failed to load data. Please check the input and try again.")
        else:
            st.session_state.list_result = list_result
            loaded_nodes, loaded_edges = data
            st.session_state.original_nodes = loaded_nodes
            st.session_state.original_edges = loaded_edges
            st.session_state.nodes = loaded_nodes
            st.session_state.edges = loaded_edges
    except ValueError as e:
        st.error(f"Berita tidak dapat diproses, mohon cek kembali input Anda dan pastikan link berita termasuk dalam daftar link yang didukung")
    except Exception as e:
        st.error(f"Berita tidak dapat diproses, mohon cek kembali input Anda")

# Memastikan variabel session state terinisialisasi
if 'original_nodes' not in st.session_state:
    st.session_state.original_nodes = []
if 'original_edges' not in st.session_state:
    st.session_state.original_edges = []
if 'list_result' not in st.session_state:
    st.session_state.list_result = []

# Fungsi untuk menghapus data
if st.button("Hapus Data"):
    # Menghapus data dengan menghapus keys dari session state
    for key in ['nodes', 'edges', 'original_nodes', 'original_edges']:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun() 

# Opsi pemilihan entitas untuk difokuskan
node_options = [node.label for node in st.session_state.get('original_nodes', []) if isinstance(node, Node) and node.color is None]
selected_nodes = st.sidebar.multiselect("Pilih entitas untuk difokuskan", node_options)

# Membuat mapping warna ke tipe informasi node
color_to_type = {
    "red": "Kutipan",
    "yellow": "Sentimen",
    "green": "5W1H",
    "black": "Kronologi",
    None: "Entitas"
}

# Membalikkan mapping untuk filtering
type_to_color = {v: k for k, v in color_to_type.items()}
# Menentukan jenis node yang tersedia berdasarkan dataset original
all_node_types = list(set(color_to_type.get(node.color, "Other") for node in st.session_state.get('original_nodes', [])))

# Jika entitas dipilih, filter jenis node yang terhubung ke entitas tersebut
if selected_nodes:
    selected_node_ids = [node.id for node in st.session_state.original_nodes if node.label in selected_nodes]
    
    # Mengumpulkan edge yang terhubung ke entity yang dipilih
    filtered_edges = [edge for edge in st.session_state.original_edges if edge.source in selected_node_ids or edge.to in selected_node_ids]
    
    # Mengumpulkan semua ID node dari edge yang terhubung
    connected_node_ids = set(edge.source for edge in filtered_edges).union(edge.to for edge in filtered_edges)
    
    # Mengumpulkan semua node yang terhubung
    connected_nodes = [node for node in st.session_state.original_nodes if node.id in connected_node_ids]
    
    # Menentukan jenis node yang tersedia berdasarkan node yang terhubung
    available_node_types = list(set(color_to_type.get(node.color, "Other") for node in connected_nodes))
else:
    # Menampilkan semua jenis node jika tidak ada entitas yang dipilih
    available_node_types = all_node_types

# Menyediakan multiselect untuk filtering berdasarkan jenis node
selected_node_types = st.sidebar.multiselect("Filter berdasarkan jenis elemen berita", available_node_types, default=available_node_types)

# Menampilkan hasil LLM dalam bentuk list di sidebar
if st.session_state.list_result:
    st.sidebar.write("Informasi yang didapat:")
    st.sidebar.write(st.session_state.list_result)

# Mengonversi kembali jenis node yang dipilih ke warna yang sesuai untuk filtering
selected_colors = [type_to_color[typ] for typ in selected_node_types]

# Menampilkan hasil KG yang telah difilter
if selected_nodes:
    filtered_nodes = [node for node in connected_nodes if node.color in selected_colors]
else:
    filtered_nodes = [node for node in st.session_state.get('original_nodes', []) if node.color in selected_colors]
    filtered_edges = st.session_state.get('original_edges', [])

# Mengupdate session state dengan node dan edge yang telah difilter
st.session_state.nodes = filtered_nodes
st.session_state.edges = filtered_edges

# Konfigurasi tampilan KG
config = Config(width=1500, height=1000, directed=True, physics=False, 
                hierarchical={
                    "enabled": True,
                    "levelSeparation": 2500,
                    "nodeSpacing": 2500,
                    "treeSpacing": 2500,
                    "parentCentralization": True,
                    "shakeTowards": "leaves"
                })
        

with st.container():
    agraph(nodes=st.session_state.get('nodes', []), edges=st.session_state.get('edges', []), config=config)
