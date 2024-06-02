import re
from streamlit_agraph import Node, Edge

def parse_markdown(markdown_content):
    nodes = []
    edges = []
    
    # Regex pattern untuk mengekstrak node dan edge
    node_pattern = re.compile(r"### Node ID: (\S+)\n\*\*Label\*\*: (.+)\n\*\*Type\*\*: (\S+)\n---")
    edge_pattern = re.compile(r"\*\*Source\*\*: (\S+)\n\*\*Target\*\*: (\S+)\n\*\*Label\*\*: (.+)\n---")
    
    # Ekstraksi node
    for match in node_pattern.finditer(markdown_content):
        node_id, label, node_type = match.groups()
        short_label = (label[:25] + '...') if len(label) > 25 else label
        chunks = [label[i:i+40] for i in range(0, len(label), 40)]
        label = '-\n'.join(chunks[:-1]) + chunks[-1]
                
        # Penetapan warna node berdasarkan tipe informasi
        if node_type == 'Entity':
            node_color = None
        elif node_type == 'Sentiment':
            node_color = 'yellow'
        elif node_type == 'Quotes':
            node_color = 'red'
        elif node_type == '5W1H':
            node_color = 'green'
        elif node_type == 'Chronology':
            node_color = 'black'
        else:
            node_color = 'blue'

        node_size = 20 


        nodes.append(Node(id=node_id.replace('_', '\_'), label=short_label, size=node_size, color=node_color, title=label, style="border: 1px solid black; cursor: pointer; padding: 5px;", type=node_type))

    # Ekstraksi edge(sisi)
    for match in edge_pattern.finditer(markdown_content):
        source, target, label = match.groups()
        chunks = [label[i:i+20] for i in range(0, len(label), 20)]
        label = '-\n'.join(chunks[:-1]) + chunks[-1]
        edges.append(Edge(source=source.replace('_', '\_'), label=label, target=target.replace('_', '\_') if target else None))

    return nodes, edges
