from llama_index import Document, ServiceContext, StorageContext, VectorStoreIndex
from llama_index.embeddings import HuggingFaceEmbedding
from llama_index.retrievers import VectorIndexRetriever
from llama_index.vector_stores import ChromaVectorStore

import chromadb

db = chromadb.PersistentClient(path="./db")
chroma_collection = db.get_or_create_collection("mediabiasfactcheck.com")
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")
service_context = ServiceContext.from_defaults(embed_model=embed_model)
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

data = ["bla", "dibla"]
documents = []
# iterate over the list of data and keep track of the index
for i, text in enumerate(data):
    # create a document with the index as id
    document = Document(doc_id=i, text=text)
    # add the document to the list
    documents.append(document)
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context, service_context=service_context
)
retriever = VectorIndexRetriever(index=index)
response = retriever.retrieve("bla")
print(response)
