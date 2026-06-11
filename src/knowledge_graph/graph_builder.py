import json
from pathlib import Path
from typing import List, Dict, Any


class KnowledgeGraphBuilder:

    def build_graph(self, enriched_chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
        nodes = []
        edges = []

        node_ids = set()
        edge_ids = set()

        for chunk in enriched_chunks:
            chunk_id = chunk["chunk_id"]
            entities = chunk.get("entities", {})

            self._add_node(
                nodes,
                node_ids,
                node_id=chunk_id,
                node_type="Chunk",
                name=chunk_id,
                properties={
                    "document_id": chunk["document_id"],
                    "text_preview": chunk["text"][:150],
                },
            )

            for company in entities.get("companies", []):
                company_id = self._normalize_id("company", company)

                self._add_node(
                    nodes,
                    node_ids,
                    node_id=company_id,
                    node_type="Company",
                    name=company,
                    properties={},
                )

                self._add_edge(
                    edges,
                    edge_ids,
                    source=chunk_id,
                    target=company_id,
                    relationship="MENTIONS",
                )

            for department in entities.get("departments", []):
                department_id = self._normalize_id("department", department)

                self._add_node(
                    nodes,
                    node_ids,
                    node_id=department_id,
                    node_type="Department",
                    name=department,
                    properties={},
                )

                self._add_edge(
                    edges,
                    edge_ids,
                    source=chunk_id,
                    target=department_id,
                    relationship="MENTIONS",
                )

            for metric in entities.get("business_metrics", []):
                metric_id = self._normalize_id("metric", metric)

                self._add_node(
                    nodes,
                    node_ids,
                    node_id=metric_id,
                    node_type="BusinessMetric",
                    name=metric,
                    properties={},
                )

                self._add_edge(
                    edges,
                    edge_ids,
                    source=chunk_id,
                    target=metric_id,
                    relationship="MENTIONS",
                )

                for company in entities.get("companies", []):
                    company_id = self._normalize_id("company", company)

                    self._add_edge(
                        edges,
                        edge_ids,
                        source=company_id,
                        target=metric_id,
                        relationship="HAS_METRIC",
                    )

        return {
            "nodes": nodes,
            "edges": edges,
            "summary": {
                "total_nodes": len(nodes),
                "total_edges": len(edges),
            },
        }

    def _add_node(
        self,
        nodes: List[Dict[str, Any]],
        node_ids: set,
        node_id: str,
        node_type: str,
        name: str,
        properties: Dict[str, Any],
    ) -> None:

        if node_id not in node_ids:
            nodes.append(
                {
                    "id": node_id,
                    "type": node_type,
                    "name": name,
                    "properties": properties,
                }
            )
            node_ids.add(node_id)

    def _add_edge(
        self,
        edges: List[Dict[str, Any]],
        edge_ids: set,
        source: str,
        target: str,
        relationship: str,
    ) -> None:

        edge_id = f"{source}_{relationship}_{target}"

        if edge_id not in edge_ids:
            edges.append(
                {
                    "source": source,
                    "target": target,
                    "relationship": relationship,
                }
            )
            edge_ids.add(edge_id)

    def _normalize_id(self, prefix: str, value: str) -> str:
        clean_value = (
            value.lower()
            .replace(" ", "_")
            .replace("%", "percent")
            .replace(".", "")
        )

        return f"{prefix}_{clean_value}"


if __name__ == "__main__":

    input_path = Path("data/processed/enriched_chunks.json")
    output_path = Path("data/processed/knowledge_graph.json")

    if not input_path.exists():
        raise FileNotFoundError(
            "enriched_chunks.json not found. Run entity_extractor.py first."
        )

    with open(input_path, "r", encoding="utf-8") as file:
        enriched_chunks = json.load(file)

    builder = KnowledgeGraphBuilder()
    graph = builder.build_graph(enriched_chunks)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(graph, file, indent=4, ensure_ascii=False)

    print("\nKnowledge Graph Builder Results")
    print("=" * 40)
    print(f"Total nodes: {graph['summary']['total_nodes']}")
    print(f"Total edges: {graph['summary']['total_edges']}")
    print(f"Output saved to: {output_path}")

    print("\nSample Nodes:")
    print(graph["nodes"][:5])

    print("\nSample Edges:")
    print(graph["edges"][:5])