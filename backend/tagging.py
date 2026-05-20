"""
Tagging Module
Automatically generates tags for documents based on content
"""

import re
from collections import Counter


# Keywords for different categories
TAG_KEYWORDS = {
    "Finance": ["invoice", "bill", "payment", "receipt", "tax", "budget", "financial", "cost", "price", "transaction", "money", "account", "balance", "expense"],
    "Career": ["resume", "cv", "job", "employment", "career", "experience", "position", "skill", "qualification", "candidate", "work", "profile"],
    "Health": ["medical", "doctor", "hospital", "patient", "health", "disease", "treatment", "prescription", "therapy", "clinic", "medicine"],
    "Legal": ["contract", "agreement", "legal", "law", "attorney", "court", "lawsuit", "clause", "terms", "conditions", "policy"],
    "Education": ["school", "university", "student", "course", "subject", "exam", "certificate", "degree", "learning", "education", "class"],
    "Technology": ["software", "code", "programming", "app", "system", "data", "network", "computer", "tech", "development"],
    "Research": ["research", "study", "analysis", "experiment", "hypothesis", "data", "methodology", "conclusion", "findings"]
}

SKILL_ALIASES = {
    "py": "python",
    "js": "javascript",
    "ts": "typescript",
    "node": "nodejs",
    "reactjs": "react",
}

SKILL_KEYWORDS = {
    "python", "javascript", "typescript", "java", "c", "c++", "c#", "go", "golang",
    "rust", "php", "ruby", "kotlin", "swift", "nodejs", "react", "angular", "vue",
    "django", "flask", "fastapi", "spring", "express", "sql", "mysql", "postgresql",
    "mongodb", "redis", "aws", "azure", "gcp", "docker", "kubernetes", "git",
    "machine learning", "tensorflow", "pytorch", "nlp", "data science"
}

STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "has", "have",
    "in", "is", "it", "of", "on", "or", "that", "the", "to", "was", "were", "will",
    "with", "this", "these", "those", "you", "your", "their", "our", "we", "they",
    "i", "he", "she", "them", "his", "her", "its", "not", "no", "yes", "can"
}


def normalize_token(token):
    """Normalize common aliases for better matching."""
    cleaned = token.strip().lower()
    return SKILL_ALIASES.get(cleaned, cleaned)


def generate_tags(text):
    """
    Generate tags based on text content
    
    Args:
        text: Document text
        
    Returns:
        List of tags
    """
    if not text:
        return []
    
    text_lower = text.lower()
    detected_tags = set()
    
    # Check for keywords in each category
    for category, keywords in TAG_KEYWORDS.items():
        for keyword in keywords:
            # Use word boundaries to match whole words
            if re.search(r'\b' + keyword + r'\b', text_lower):
                detected_tags.add(category)
                break  # Only add category once
    
    return sorted(list(detected_tags))


def detect_skills(text):
    """
    Detect technical skills present in a document.
    """
    if not text:
        return []

    text_lower = text.lower()
    found = set()

    for skill in SKILL_KEYWORDS:
        if " " in skill:
            if skill in text_lower:
                found.add(skill)
            continue

        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text_lower):
            found.add(skill)

    # Include alias-driven detection for short forms such as py/js.
    for raw in re.findall(r"[a-zA-Z0-9+#.]+", text_lower):
        normalized = normalize_token(raw)
        if normalized in SKILL_KEYWORDS:
            found.add(normalized)

    return sorted(found)


def extract_topic_keywords(text, limit=20):
    """
    Extract frequent topic keywords from a document for topic search.
    """
    if not text:
        return []

    tokens = []
    for token in re.findall(r"[a-zA-Z0-9+#.]{3,}", text.lower()):
        normalized = normalize_token(token)
        if normalized in STOPWORDS:
            continue
        if normalized.isdigit():
            continue
        tokens.append(normalized)

    if not tokens:
        return []

    counts = Counter(tokens)
    return [word for word, _ in counts.most_common(limit)]


def get_tag_suggestions(text):
    """
    Get tag suggestions with confidence scores
    
    Args:
        text: Document text
        
    Returns:
        Dictionary with tags and their confidence scores
    """
    if not text:
        return {}
    
    text_lower = text.lower()
    tag_scores = {}
    
    # Score each category
    for category, keywords in TAG_KEYWORDS.items():
        score = 0
        for keyword in keywords:
            if re.search(r'\b' + keyword + r'\b', text_lower):
                score += 1
        
        if score > 0:
            # Calculate confidence (0-100)
            confidence = (score / len(keywords)) * 100
            tag_scores[category] = round(confidence, 1)
    
    # Sort by confidence
    sorted_tags = dict(sorted(tag_scores.items(), key=lambda x: x[1], reverse=True))
    
    return sorted_tags


def add_custom_tag(existing_tags, new_tag):
    """
    Add a custom tag to existing tags
    
    Args:
        existing_tags: List of existing tags
        new_tag: Tag to add
        
    Returns:
        Updated list of tags
    """
    if new_tag not in existing_tags:
        existing_tags.append(new_tag)
    
    return sorted(existing_tags)


def remove_tag(existing_tags, tag_to_remove):
    """
    Remove a tag from existing tags
    
    Args:
        existing_tags: List of existing tags
        tag_to_remove: Tag to remove
        
    Returns:
        Updated list of tags
    """
    return [tag for tag in existing_tags if tag != tag_to_remove]
