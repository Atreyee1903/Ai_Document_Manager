"""
Search Module
Keyword/topic-focused document search
"""

import os
import re
from .tagging import normalize_token, extract_topic_keywords
from .utils.file_handler import get_user_extracted_text_dir, get_user_documents_dir


STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "has", "have",
    "in", "is", "it", "of", "on", "or", "that", "the", "to", "was", "were", "will",
    "with", "this", "these", "those", "i", "we", "you", "they", "he", "she", "them"
}

DOC_EXTENSIONS = [".pdf", ".docx", ".jpg", ".jpeg", ".png"]


def _extract_query_terms(query):
    """Extract normalized keyword terms from query."""
    raw_tokens = re.findall(r"[a-zA-Z0-9+#.]+", query.lower())
    normalized = []
    for token in raw_tokens:
        if token in STOPWORDS:
            continue
        term = normalize_token(token)
        if len(term) < 2:
            continue
        normalized.append(term)

    # Preserve order while removing duplicates.
    deduped_terms = list(dict.fromkeys(normalized))
    require_all_terms = " and " in query.lower()
    return deduped_terms, require_all_terms


def _count_term_occurrences(content, term):
    if re.fullmatch(r"[a-z0-9]+", term):
        pattern = r"\b" + re.escape(term) + r"\b"
        return len(re.findall(pattern, content))
    return content.count(term)


def _resolve_document_filename(extracted_filename, user_id):
    """Map extracted text file to original document filename."""
    base_name = extracted_filename.replace(".txt", "")
    user_documents_dir = get_user_documents_dir(user_id)
    for ext in DOC_EXTENSIONS:
        candidate = os.path.join(user_documents_dir, f"{base_name}{ext}")
        if os.path.exists(candidate):
            return f"{base_name}{ext}"
    return base_name


def keyword_search(query, user_id, search_in_extracted=True, top_k=10):
    """
    Perform keyword-based search

    Args:
        query: Search query string
        user_id: User ID
        search_in_extracted: Whether to search in extracted_text folder

    Returns:
        List of matching files
    """
    results = []
    query_lower = query.lower().strip()
    terms, require_all_terms = _extract_query_terms(query_lower)

    if not query_lower:
        return []
    if not terms:
        terms = [query_lower]

    user_extracted_text_dir = get_user_extracted_text_dir(user_id)

    if search_in_extracted and os.path.exists(user_extracted_text_dir):
        for filename in os.listdir(user_extracted_text_dir):
            try:
                filepath = os.path.join(user_extracted_text_dir, filename)
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read().lower()

                    full_query_hits = _count_term_occurrences(content, query_lower)
                    matched_terms = []
                    term_occurrences = 0
                    for term in terms:
                        count = _count_term_occurrences(content, term)
                        if count > 0:
                            matched_terms.append(term)
                            term_occurrences += count

                    if require_all_terms and len(matched_terms) < len(terms):
                        continue

                    if full_query_hits == 0 and not matched_terms:
                        continue

                    # Build relevance score with phrase+term boosts.
                    relevance = (full_query_hits * 80) + (term_occurrences * 10) + (len(matched_terms) * 20)
                    if require_all_terms and len(matched_terms) == len(terms):
                        relevance += 100

                    preview_start = content.find(query_lower)
                    if preview_start < 0 and matched_terms:
                        preview_start = content.find(matched_terms[0])
                    if preview_start < 0:
                        preview_start = 0
                    preview = content[preview_start:preview_start + 240]

                    results.append({
                        "file": _resolve_document_filename(filename, user_id),
                        "type": "topic_keyword",
                        "relevance": relevance,
                        "matched_keywords": matched_terms,
                        "match_ratio": round(len(matched_terms) / max(len(terms), 1), 3),
                        "preview": preview
                    })
            except Exception as e:
                print(f"Error searching in {filename}: {str(e)}")

    # Sort by relevance (occurrences)
    results.sort(key=lambda x: x["relevance"], reverse=True)

    return results[:max(1, top_k)]


def semantic_search(query, user_id, top_k=5, threshold=0.3):
    """
    Perform semantic search using embeddings

    Args:
        query: Search query string
        user_id: User ID
        top_k: Number of top results to return
        threshold: Similarity threshold (0-1)

    Returns:
        List of matching files with similarity scores
    """
    # Semantic model-based search removed in favor of scalable topic/keyword search.
    return keyword_search(query, user_id, top_k=top_k)


def combined_search(query, user_id, use_keyword=True, use_semantic=True, top_k=10):
    """
    Perform combined keyword and semantic search

    Args:
        query: Search query
        user_id: User ID
        use_keyword: Whether to include keyword search
        use_semantic: Whether to include semantic search
        top_k: Number of top results

    Returns:
        Combined results list
    """
    # Combined mode now resolves to keyword/topic search.
    return keyword_search(query, user_id, top_k=top_k)


def get_similar_documents(filename, user_id, top_k=5):
    """
    Find documents similar to a given document

    Args:
        filename: Reference document filename
        user_id: User ID
        top_k: Number of similar documents to return

    Returns:
        List of similar documents
    """
    try:
        source_base = os.path.splitext(filename)[0]
        user_extracted_text_dir = get_user_extracted_text_dir(user_id)
        source_path = os.path.join(user_extracted_text_dir, f"{source_base}.txt")
        if not os.path.exists(source_path):
            return []

        with open(source_path, "r", encoding="utf-8", errors="ignore") as f:
            source_terms = set(extract_topic_keywords(f.read(), limit=80))
        if not source_terms:
            return []

        results = []
        for extracted_file in os.listdir(user_extracted_text_dir):
            if extracted_file == f"{source_base}.txt":
                continue

            candidate_path = os.path.join(user_extracted_text_dir, extracted_file)
            with open(candidate_path, "r", encoding="utf-8", errors="ignore") as f:
                candidate_terms = set(extract_topic_keywords(f.read(), limit=80))

            if not candidate_terms:
                continue

            union_size = len(source_terms | candidate_terms)
            if union_size == 0:
                continue
            overlap = len(source_terms & candidate_terms)
            similarity = overlap / union_size
            if similarity <= 0:
                continue

            results.append({
                "file": _resolve_document_filename(extracted_file, user_id),
                "similarity": round(similarity, 3)
            })

        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results[:max(1, top_k)]
    except Exception as e:
        print(f"Error finding similar documents: {str(e)}")
        return []
