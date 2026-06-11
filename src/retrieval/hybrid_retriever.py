import json
from pathlib import Path
from typing import List, Dict, Any

from semantic_search import SemanticSearchEngine


class HybridRetriever:

    def __init__(
        self,
        graph_path: str = "data/processed/knowledge_graph.json"
    ):
        self.semantic_search = SemanticSearchEngine()
        self.graph_path = Path(graph_path)

        if not self.graph_path.exists():
            raise FileNotFoundError("knowledge_graph.json not found.")

        with open(self.graph_path, "r", encoding="utf-8") as file:
            self.graph = json.load(file)

    def retrieve(self, query: str, top_k: int = 3) -> Dict[str, Any]:
        vector_results = self.semantic_search.search(query, top_k=top_k)
        graph_results = self._graph_search(query)

        return {
            "query": query,
            "vector_results": vector_results,
            "graph_results": graph_results,
            "retrieval_strategy": "hybrid_vector_plus_graph",
        }

    def _graph_search(self, query: str) -> Dict[str, Any]:
        query_lower = query.lower()

        query_keywords = set(
            word.strip(".,?!")
            for word in query_lower.split()
            if len(word) > 3
        )

        matched_nodes = []
        matched_edges = []

        for node in self.graph["nodes"]:
            node_name_lower = node["name"].lower()

            node_keywords = set(
                word.strip(".,?!")
                for word in node_name_lower.split()
                if len(word) > 3
            )

            keyword_overlap = query_keywords.intersection(node_keywords)

            if keyword_overlap:
                matched_nodes.append(
                    {
                        **node,
                        "matched_keywords": list(keyword_overlap),
                    }
                )

        matched_node_ids = {node["id"] for node in matched_nodes}

        for edge in self.graph["edges"]:
            if edge["source"] in matched_node_ids or edge["target"] in matched_node_ids:
                matched_edges.append(edge)

        return {
            "matched_nodes": matched_nodes,
            "matched_edges": matched_edges,
        }


if __name__ == "__main__":

    retriever = HybridRetriever()

    query = "What happened to customer satisfaction and revenue?"

    results = retriever.retrieve(query, top_k=2)

    print("\nHybrid Retrieval Results")
    print("=" * 40)
    print(f"Query: {results['query']}")
    print(f"Strategy: {results['retrieval_strategy']}")

    print("\nVector Results:")
    for index, result in enumerate(results["vector_results"], start=1):
        print(f"\nVector Result {index}")
        print("-" * 30)
        print(f"Score: {result['score']:.4f}")
        print(f"Text: {result['text']}")
        print(f"Entities: {result['entities']}")

    print("\nGraph Results:")
    print(json.dumps(results["graph_results"], indent=4))