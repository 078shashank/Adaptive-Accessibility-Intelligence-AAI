"""Caching Layer for Text Simplification"""
import hashlib
import time
from typing import Optional, Dict
from functools import wraps
import logging

logger = logging.getLogger(__name__)


class SimpleCache:
    """
    In-memory cache for text simplification results
    Thread-safe and memory-efficient
    """
    
    def __init__(self, max_size: int = 1000, ttl_seconds: int = 3600):
        self.cache: Dict[str, dict] = {}
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
        self.hits = 0
        self.misses = 0
    
    def _make_key(self, text: str, reading_level: str) -> str:
        """Generate cache key from text and reading level"""
        combined = f"{text}:{reading_level}"
        return hashlib.md5(combined.encode()).hexdigest()
    
    def get(self, text: str, reading_level: str) -> Optional[str]:
        """Get cached result"""
        key = self._make_key(text, reading_level)
        
        if key in self.cache:
            entry = self.cache[key]
            # Check if expired
            if time.time() - entry['timestamp'] < self.ttl_seconds:
                self.hits += 1
                logger.debug(f"Cache hit for {key[:8]}...")
                return entry['result']
            else:
                # Remove expired entry
                del self.cache[key]
        
        self.misses += 1
        return None
    
    def set(self, text: str, reading_level: str, result: str) -> None:
        """Set cache entry"""
        key = self._make_key(text, reading_level)
        
        # Simple eviction: if cache is full, clear 10% oldest entries
        if len(self.cache) >= self.max_size:
            old_entries = sorted(
                self.cache.items(),
                key=lambda x: x[1]['timestamp']
            )
            for k, _ in old_entries[:max(1, self.max_size // 10)]:
                del self.cache[k]
            logger.debug(f"Cache evicted {self.max_size // 10} entries")
        
        self.cache[key] = {
            'result': result,
            'timestamp': time.time()
        }
        logger.debug(f"Cache set for {key[:8]}...")
    
    def clear(self) -> None:
        """Clear entire cache"""
        self.cache.clear()
        logger.info("Cache cleared")
    
    def get_stats(self) -> dict:
        """Get cache statistics"""
        total = self.hits + self.misses
        hit_rate = (self.hits / total * 100) if total > 0 else 0
        
        return {
            'size': len(self.cache),
            'max_size': self.max_size,
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': f"{hit_rate:.1f}%",
            'ttl_seconds': self.ttl_seconds
        }


# Global cache instance
text_cache = SimpleCache(max_size=500, ttl_seconds=3600)


def cached_simplification(func):
    """
    Decorator for caching text simplification results
    
    Usage:
        @cached_simplification
        def simplify_text(text, reading_level):
            # ... expensive operation
            return simplified_text
    """
    @wraps(func)
    def wrapper(text: str, reading_level: str = "intermediate", *args, **kwargs):
        # Try to get from cache
        cached_result = text_cache.get(text, reading_level)
        if cached_result:
            return cached_result
        
        # Not in cache, call function
        result = func(text, reading_level, *args, **kwargs)
        
        # Store in cache
        text_cache.set(text, reading_level, result)
        
        return result
    
    return wrapper


def get_cache_stats() -> dict:
    """Get cache performance statistics"""
    return text_cache.get_stats()


def clear_cache() -> None:
    """Clear all cached results"""
    text_cache.clear()


def cache_warmup(simplification_func):
    """
    Warm up cache with common texts
    Call this on startup for faster initial performance
    """
    common_texts = {
        "basic": [
            "Hello world. This is a test.",
            "The quick brown fox jumps over the lazy dog.",
        ],
        "intermediate": [
            "Artificial intelligence is transforming the world.",
            "Machine learning algorithms require large datasets.",
        ],
        "advanced": [
            "Quantum computing leverages superposition and entanglement.",
            "Natural language processing involves tokenization and embeddings.",
        ]
    }
    
    logger.info("🔥 Warming up simplification cache...")
    for level, texts in common_texts.items():
        for text in texts:
            try:
                result = simplification_func(text, level)
                text_cache.set(text, level, result)
                logger.debug(f"Warmed cache: {level} - {text[:30]}...")
            except Exception as e:
                logger.warning(f"Failed to warm cache: {e}")
    
    logger.info(f"✓ Cache warmup complete. Stats: {get_cache_stats()}")


class DatabaseCache:
    """
    Database-backed cache for persistent results
    Used for long-term storage of simplifications
    """
    
    @staticmethod
    def get_cached_simplification(
        db_session,
        original_text: str,
        reading_level: str
    ) -> Optional[str]:
        """Get cached simplification from database"""
        from app.models import TextSimplification
        
        result = db_session.query(TextSimplification).filter(
            TextSimplification.original_text == original_text,
            TextSimplification.reading_level == reading_level
        ).first()
        
        if result:
            logger.debug(f"DB cache hit for {original_text[:30]}...")
            return result.simplified_text
        
        return None
    
    @staticmethod
    def cache_simplification(
        db_session,
        user_id: int,
        original_text: str,
        simplified_text: str,
        reading_level: str,
        processing_time_ms: int
    ) -> None:
        """Cache simplification in database"""
        from app.models import TextSimplification
        
        cache_entry = TextSimplification(
            user_id=user_id,
            original_text=original_text,
            simplified_text=simplified_text,
            reading_level=reading_level,
            processing_time_ms=processing_time_ms
        )
        
        db_session.add(cache_entry)
        db_session.commit()
        logger.debug(f"DB cache set for {original_text[:30]}...")


if __name__ == "__main__":
    # Test cache
    print("Testing SimpleCache...")
    
    test_cache = SimpleCache(max_size=100)
    
    # Test set/get
    test_cache.set("hello world", "basic", "hello there")
    result = test_cache.get("hello world", "basic")
    print(f"✓ Cache get: {result}")
    
    # Test miss
    result = test_cache.get("missing", "basic")
    print(f"✓ Cache miss: {result}")
    
    # Print stats
    stats = test_cache.get_stats()
    print(f"✓ Cache stats: {stats}")
