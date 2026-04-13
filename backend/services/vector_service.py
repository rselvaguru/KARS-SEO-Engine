"""
Vector Service - Semantic Search Engine
Manages embeddings and semantic similarity matching using ChromaDB
"""

import chromadb
import logging
from typing import List, Dict
from pathlib import Path

logger = logging.getLogger(__name__)

# Initialize ChromaDB client (persistent local storage)
DB_PATH = str(Path(__file__).parent.parent / "chroma_db")
client = chromadb.PersistentClient(path=DB_PATH)

# Get or create collection
try:
    collection = client.get_or_create_collection(
        name="seo_content",
        metadata={"hnsw:space": "cosine"}
    )
    logger.info("ChromaDB collection 'seo_content' initialized")
except Exception as e:
    logger.error(f"Failed to initialize ChromaDB: {e}")
    collection = None


class VectorService:
    """Manages vector embeddings and semantic search"""

    @staticmethod
    def add_document(doc_id: str, content: str, metadata: Dict = None) -> bool:
        """
        Add or update a document in vector DB
        
        Args:
            doc_id: Unique document identifier
            content: Document text for embedding
            metadata: Optional metadata dict
        
        Returns:
            Success status
        """
        try:
            if not collection:
                logger.warning("ChromaDB collection not available")
                return False

            # Truncate content to reasonable length for embedding
            content_for_embedding = content[:8000]
            
            collection.upsert(
                ids=[doc_id],
                documents=[content_for_embedding],
                metadatas=[metadata or {"source": "seo_content"}]
            )
            
            logger.info(f"Document {doc_id} added to vector DB")
            return True
            
        except Exception as e:
            logger.error(f"Error adding document to vector DB: {e}")
            return False

    @staticmethod
    def get_similar(query_text: str, n: int = 5, threshold: float = 0.3) -> List[Dict]:
        """
        Find semantically similar documents
        
        Args:
            query_text: Text to find similar documents for
            n: Number of results
            threshold: Minimum similarity score (0-1)
        
        Returns:
            List of similar documents with scores
        """
        try:
            if not collection:
                logger.warning("ChromaDB collection not available")
                return []

            # Query the collection
            results = collection.query(
                query_texts=[query_text[:8000]],
                n_results=n
            )

            # Format results
            similar_docs = []
            if results and results["ids"] and len(results["ids"]) > 0:
                for i, doc_id in enumerate(results["ids"][0]):
                    distance = results["distances"][0][i] if results["distances"] else 0
                    # Convert distance to similarity (cosine distance to similarity)
                    similarity = 1 - distance
                    
                    if similarity >= threshold:
                        similar_docs.append({
                            "id": doc_id,
                            "similarity": round(similarity, 3),
                            "metadata": results["metadatas"][0][i] if results["metadatas"] else {}
                        })
            
            logger.info(f"Found {len(similar_docs)} similar documents")
            return similar_docs

        except Exception as e:
            logger.error(f"Error querying similar documents: {e}")
            return []

    @staticmethod
    def delete_document(doc_id: str) -> bool:
        """Remove document from vector DB"""
        try:
            if not collection:
                return False
            
            collection.delete(ids=[doc_id])
            logger.info(f"Document {doc_id} deleted from vector DB")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting document: {e}")
            return False

    @staticmethod
    def get_collection_stats() -> Dict:
        """Get statistics about the collection"""
        try:
            if not collection:
                return {"status": "unavailable"}
            
            count = collection.count()
            return {
                "status": "available",
                "documents": count,
                "collection": "seo_content"
            }
            
        except Exception as e:
            logger.error(f"Error getting collection stats: {e}")
            return {"status": "error", "message": str(e)}
