import json
from pathlib import Path

from pyvis.network import Network


class KnowledgeGraphVisualizer:

    def __init__(
        self,
        graph_path: str = "data/processed/knowledge_graph.json",
        output_path: str = "data/processed/knowledge_graph.html",
    ):
        self.graph_path = Path(graph_path)
        self.output_path = Path(output_path)

    def generate(self):
        if not self.graph_path.exists():
            raise FileNotFoundError("knowledge_graph.json not found.")

        with open(self.graph_path, "r", encoding="utf-8") as file:
            graph = json.load(file)

        network = Network(
            height="650px",
            width="100%",
            bgcolor="#111827",
            font_color="white",
            directed=True,
        )

        for node in graph["nodes"]:
            network.add_node(
                node["id"],
                label=node["name"],
                title=node["type"],
                group=node["type"],
            )

        for edge in graph["edges"]:
            network.add_edge(
                edge["source"],
                edge["target"],
                label=edge["relationship"],
            )

        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        network.write_html(str(self.output_path))

        print("\nKnowledge Graph Visualization Created")
        print("=" * 50)
        print(f"Output saved to: {self.output_path}")

        return self.output_path


if __name__ == "__main__":
    visualizer = KnowledgeGraphVisualizer()
    visualizer.generate()