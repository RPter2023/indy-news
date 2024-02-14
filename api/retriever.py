from typing import List

from llama_index.core.retrievers import BaseRetriever, VectorIndexRetriever
from llama_index.core.schema import NodeWithScore, QueryType
from llama_index.retrievers.bm25 import BM25Retriever


class HybridRetriever(BaseRetriever):
    vector_retriever: VectorIndexRetriever
    bm25_retriever: BM25Retriever

    def __init__(
        self, vector_retriever: VectorIndexRetriever, bm25_retriever: BM25Retriever
    ):
        self.vector_retriever = vector_retriever
        self.bm25_retriever = bm25_retriever
        super().__init__()

    def _retrieve(self, query_bundle: QueryType) -> List[NodeWithScore]:
        bm25_nodes = self.bm25_retriever.retrieve(query_bundle)
        vector_nodes = self.vector_retriever.retrieve(query_bundle)

        # combine the two lists of nodes
        all_nodes: List[NodeWithScore] = []
        node_ids = set()
        for n in bm25_nodes + vector_nodes:
            if n.node.node_id not in node_ids:
                all_nodes.append(n)
                node_ids.add(n.node.node_id)
        return all_nodes
