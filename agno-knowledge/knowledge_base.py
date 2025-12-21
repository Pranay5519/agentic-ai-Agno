from agno.knowledge.reader.pdf_reader import PDFReader
from agno.knowledge.reader.pdf_reader import PDFReader
from agno.knowledge.chunking.semantic import SemanticChunking
from agno.knowledge.embedder.sentence_transformer import SentenceTransformerEmbedder
from agno.vectordb.lancedb import LanceDb
from agno.knowledge.knowledge import Knowledge
from dotenv import load_dotenv
load_dotenv()

embedder = SentenceTransformerEmbedder()

# define the chunking strategy
chunking_strategy = SemanticChunking(embedder=embedder,
                                     chunk_size=1000)

# create the pdf reader
reader = PDFReader(chunking_strategy=chunking_strategy)


# create the vector db
vector_db = LanceDb(uri="agno-knowledge/vector_db/lancedb",
                    embedder=embedder,
                    table_name="knowledge_table")

# create a knowledge base
knowledge_base = Knowledge(name="Knowledge_Base",
                           description="Contains the research paper 'Attention is all you need'",
                           vector_db=vector_db)

if __name__ == "__main__":
    # add content to the knowledge base
    knowledge_base.add_content(path=r"D:\agno-basics\agno-knowledge\tubetalk_Progress.pdf",
                            reader=reader)