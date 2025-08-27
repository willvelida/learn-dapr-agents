from dapr_agents import Agent
from dapr_agents.document.embedder.sentence import SentenceTransformerEmbedder
from dapr_agents.storage.vectorstores import ChromaVectorStore
from dapr_agents.tool import tool
from dapr_agents.types.document import Document
from dotenv import load_dotenv
import asyncio
import logging
import json

logging.basicConfig(level=logging.INFO)
load_dotenv()

# Setup embedding function and persistent vector store
embedding_function = SentenceTransformerEmbedder(model="all-MiniLM-L6-v2")
vector_store = ChromaVectorStore(
    name="quote_vectorstore",
    embedding_function=embedding_function,
    persistent=True,  # Data persists between runs
    path="./quote_db"
)

# Tool to search for similar documents using semantic search
@tool
def search_quotes(query: str) -> str:
    """Search for quote documents in the vector store"""
    results = vector_store.search_similar(query_texts=query, k=3)
    docs = results.get("documents", [])
    metadatas = results.get("metadatas", [])
    if not docs:
        return f"No quotes found for: '{query}'"
    return "\n---\n".join([f"Quote: {doc}\nMetadata: {meta}" for doc, meta in zip(docs,metadatas)])

# Tool to add new documents to the vector store
@tool
def add_quote(content: str, metadata: str = "") -> str:
    """Add a quote document to the vector store"""
    try:
        meta = json.loads(metadata) if metadata else {}
    except Exception:
        meta = {"info": metadata}
    doc = Document(text=content, metadata=meta)
    ids = vector_store.add_documents(documents=[doc])
    return f"Added quote with ID {ids[0]}" if ids else "Quote added (no ID returned)"

async def main():
    logging.info("Starting QuoteFinderAgent application")
    
    # Seed the vector store with initial famous quotes
    quotes = [
        Document(text="May the force be with you.", metadata={"character": "Obi-Wan", "movie": "Star Wars"}),
        Document(text="I'll be back", metadata={"character": "Terminator", "movie": "The Terminator"}),
        Document(text="Why so serious?", metadata={"character": "Joker", "movie": "The Dark Knight"})
    ]
    logging.info("Seeding vector store with initial documents...")
    vector_store.add_documents(quotes)
    logging.info(f"Seeded {len(quotes)} initial documents")

    # Create the agent with vector store capabilities
    logging.info("Creating QuoteFinderAgent...")
    agent = Agent(
        name="QuoteFinderAgent",
        role="Movie Quote Assistant",
        goal="Find and store famous movie quotes",
        instructions=[
            "Search quotes by meaning or keywords",
            "Add new quotes with metadata",
        ],
        tools=[search_quotes,add_quote],  # Provide search and add tools
        vector_store=vector_store  # Connect the vector store to the agent
    )
    logging.info("Agent created successfully")

    # Run agent interactions to demonstrate capabilities
    logging.info("Running agent interactions...")
    print(await agent.run("Search for quotes about the force"))
    print(await agent.run("Add quote: 'I am your father' with metadata: {\"character\": \"Darth Vader\", \"movie\": \"Star Wars\"}"))
    print(await agent.run("Search for quotes from Star Wars"))
    logging.info("Application completed successfully")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nInterrupted by user. Exiting gracefully...")
    except Exception as e:
        print(f"\nError occurred: {e}")
        