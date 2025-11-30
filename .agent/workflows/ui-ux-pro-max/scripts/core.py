#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UI/UX Pro Max Core - Shared components for search and plan generation
"""

import csv
import re
from pathlib import Path
from math import log
from collections import defaultdict

# ============ CONFIGURATION ============
DATA_DIR = Path(__file__).parent.parent / "data"
MAX_RESULTS = 5

CSV_CONFIG = {
    "style": {
        "file": "styles.csv",
        "search_cols": ["Style Category", "Keywords", "Best For", "Type"],
        "output_cols": ["Style Category", "Type", "Keywords", "Primary Colors", "Effects & Animation", "Best For", "Performance", "Accessibility", "Framework Compatibility", "Complexity"]
    },
    "prompt": {
        "file": "prompts.csv",
        "search_cols": ["Style Category", "AI Prompt Keywords (Copy-Paste Ready)", "CSS/Technical Keywords"],
        "output_cols": ["Style Category", "AI Prompt Keywords (Copy-Paste Ready)", "CSS/Technical Keywords", "Implementation Checklist"]
    },
    "color": {
        "file": "colors.csv",
        "search_cols": ["Product Type", "Keywords", "Notes"],
        "output_cols": ["Product Type", "Keywords", "Primary (Hex)", "Secondary (Hex)", "CTA (Hex)", "Background (Hex)", "Text (Hex)", "Border (Hex)", "Notes"]
    },
    "chart": {
        "file": "charts.csv",
        "search_cols": ["Data Type", "Keywords", "Best Chart Type", "Accessibility Notes"],
        "output_cols": ["Data Type", "Keywords", "Best Chart Type", "Secondary Options", "Color Guidance", "Accessibility Notes", "Library Recommendation", "Interactive Level"]
    },
    "landing": {
        "file": "landing.csv",
        "search_cols": ["Pattern Name", "Keywords", "Conversion Optimization", "Section Order"],
        "output_cols": ["Pattern Name", "Keywords", "Section Order", "Primary CTA Placement", "Color Strategy", "Conversion Optimization"]
    },
    "product": {
        "file": "products.csv",
        "search_cols": ["Product Type", "Keywords", "Primary Style Recommendation", "Key Considerations"],
        "output_cols": ["Product Type", "Keywords", "Primary Style Recommendation", "Secondary Styles", "Landing Page Pattern", "Dashboard Style (if applicable)", "Color Palette Focus"]
    },
    "quick": {
        "file": "quick-ref.csv",
        "search_cols": ["Style Name", "Best For", "Category"],
        "output_cols": ["Style Name", "Type", "Best For", "Primary Colors", "Performance", "Accessibility", "Mobile", "Dark Mode"]
    },
    "ux": {
        "file": "ux-guidelines.csv",
        "search_cols": ["Category", "Issue", "Description", "Platform"],
        "output_cols": ["Category", "Issue", "Platform", "Description", "Do", "Don't", "Code Example Good", "Code Example Bad", "Severity"]
    },
    "typography": {
        "file": "typography.csv",
        "search_cols": ["Font Pairing Name", "Category", "Mood/Style Keywords", "Best For", "Heading Font", "Body Font"],
        "output_cols": ["Font Pairing Name", "Category", "Heading Font", "Body Font", "Mood/Style Keywords", "Best For", "Google Fonts URL", "CSS Import", "Tailwind Config", "Notes"]
    }
}

# Stack-specific configurations (separate from main CSV_CONFIG)
STACK_CONFIG = {
    "html-tailwind": {
        "file": "stacks/html-tailwind.csv",
        "search_cols": ["Category", "Guideline", "Description", "Do", "Don't"],
        "output_cols": ["Category", "Guideline", "Description", "Do", "Don't", "Code Good", "Code Bad", "Severity", "Docs URL"]
    },
    "react": {
        "file": "stacks/react.csv",
        "search_cols": ["Category", "Guideline", "Description", "Do", "Don't"],
        "output_cols": ["Category", "Guideline", "Description", "Do", "Don't", "Code Good", "Code Bad", "Severity", "Docs URL"]
    },
    "nextjs": {
        "file": "stacks/nextjs.csv",
        "search_cols": ["Category", "Guideline", "Description", "Do", "Don't"],
        "output_cols": ["Category", "Guideline", "Description", "Do", "Don't", "Code Good", "Code Bad", "Severity", "Docs URL"]
    },
    "vue": {
        "file": "stacks/vue.csv",
        "search_cols": ["Category", "Guideline", "Description", "Do", "Don't"],
        "output_cols": ["Category", "Guideline", "Description", "Do", "Don't", "Code Good", "Code Bad", "Severity", "Docs URL"]
    },
    "svelte": {
        "file": "stacks/svelte.csv",
        "search_cols": ["Category", "Guideline", "Description", "Do", "Don't"],
        "output_cols": ["Category", "Guideline", "Description", "Do", "Don't", "Code Good", "Code Bad", "Severity", "Docs URL"]
    },
    "swiftui": {
        "file": "stacks/swiftui.csv",
        "search_cols": ["Category", "Guideline", "Description", "Do", "Don't"],
        "output_cols": ["Category", "Guideline", "Description", "Do", "Don't", "Code Good", "Code Bad", "Severity", "Docs URL"]
    },
    "react-native": {
        "file": "stacks/react-native.csv",
        "search_cols": ["Category", "Guideline", "Description", "Do", "Don't"],
        "output_cols": ["Category", "Guideline", "Description", "Do", "Don't", "Code Good", "Code Bad", "Severity", "Docs URL"]
    },
    "flutter": {
        "file": "stacks/flutter.csv",
        "search_cols": ["Category", "Guideline", "Description", "Do", "Don't"],
        "output_cols": ["Category", "Guideline", "Description", "Do", "Don't", "Code Good", "Code Bad", "Severity", "Docs URL"]
    }
}

AVAILABLE_STACKS = list(STACK_CONFIG.keys())


# ============ BM25 IMPLEMENTATION ============
class BM25:
    """BM25 ranking algorithm for text search"""

    def __init__(self, k1=1.5, b=0.75):
        self.k1 = k1
        self.b = b
        self.corpus = []
        self.doc_lengths = []
        self.avgdl = 0
        self.idf = {}
        self.doc_freqs = defaultdict(int)
        self.N = 0

    def tokenize(self, text):
        """Lowercase, split, remove punctuation, filter short words"""
        text = str(text).lower()
        text = re.sub(r'[^\w\s]', ' ', text)
        return [w for w in text.split() if len(w) > 2]

    def fit(self, documents):
        """Build BM25 index from documents"""
        self.corpus = [self.tokenize(doc) for doc in documents]
        self.N = len(self.corpus)
        if self.N == 0:
            return
        self.doc_lengths = [len(doc) for doc in self.corpus]
        self.avgdl = sum(self.doc_lengths) / self.N

        for doc in self.corpus:
            seen = set()
            for word in doc:
                if word not in seen:
                    self.doc_freqs[word] += 1
                    seen.add(word)

        for word, freq in self.doc_freqs.items():
            self.idf[word] = log((self.N - freq + 0.5) / (freq + 0.5) + 1)

    def score(self, query):
        """Score all documents against query"""
        query_tokens = self.tokenize(query)
        scores = []

        for idx, doc in enumerate(self.corpus):
            score = 0
            doc_len = self.doc_lengths[idx]
            term_freqs = defaultdict(int)
            for word in doc:
                term_freqs[word] += 1

            for token in query_tokens:
                if token in self.idf:
                    tf = term_freqs[token]
                    idf = self.idf[token]
                    numerator = tf * (self.k1 + 1)
                    denominator = tf + self.k1 * (1 - self.b + self.b * doc_len / self.avgdl)
                    score += idf * numerator / denominator

            scores.append((idx, score))

        return sorted(scores, key=lambda x: x[1], reverse=True)


# ============ UTILITY FUNCTIONS ============
def load_csv(filepath):
    """Load CSV and return list of dicts"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def regex_search(data, query, search_cols):
    """Exact/regex matching for specific patterns"""
    pattern = re.compile(re.escape(query), re.IGNORECASE)
    results = []
    for idx, row in enumerate(data):
        for col in search_cols:
            if col in row and pattern.search(str(row[col])):
                results.append((idx, 100))
                break
    return results


def detect_domain(query):
    """Auto-detect the most relevant domain from query"""
    query_lower = query.lower()

    domain_keywords = {
        "color": ["color", "palette", "hex", "#", "rgb", "financial", "sales", "marketing", "healthcare", "it", "devops", "hr"],
        "chart": ["chart", "graph", "visualization", "trend", "bar", "pie", "scatter", "heatmap", "funnel", "gauge", "line"],
        "landing": ["landing", "page", "cta", "conversion", "hero", "testimonial", "form", "pricing", "section"],
        "product": ["saas", "ecommerce", "e-commerce", "fintech", "healthcare", "gaming", "portfolio", "agency", "crypto", "social", "productivity"],
        "prompt": ["prompt", "css", "implementation", "variable", "checklist", "code", "tailwind", "styled"],
        "quick": ["quick", "summary", "overview", "all styles", "list", "compare"],
        "style": ["style", "design", "ui", "minimalism", "glassmorphism", "neumorphism", "brutalism", "dark mode", "flat", "3d", "aurora", "retro"],
        "ux": ["ux", "user experience", "usability", "accessibility", "wcag", "touch", "scroll", "animation", "focus", "keyboard", "screen reader", "loading", "error", "validation", "feedback", "navigation", "mobile", "responsive", "performance", "z-index", "overflow"]
    }

    scores = {domain: 0 for domain in domain_keywords}
    for domain, keywords in domain_keywords.items():
        for keyword in keywords:
            if keyword in query_lower:
                scores[domain] += 1

    best_domain = max(scores, key=scores.get)
    return best_domain if scores[best_domain] > 0 else "style"


def search_domain(query, domain, max_results=MAX_RESULTS):
    """Search a specific domain and return results"""
    config = CSV_CONFIG.get(domain)
    if not config:
        return []

    filepath = DATA_DIR / config["file"]
    if not filepath.exists():
        return []

    data = load_csv(filepath)
    search_cols = config["search_cols"]
    output_cols = config["output_cols"]

    documents = []
    for row in data:
        doc_text = " ".join(str(row.get(col, "")) for col in search_cols)
        documents.append(doc_text)

    bm25 = BM25()
    bm25.fit(documents)
    bm25_results = bm25.score(query)

    regex_results = regex_search(data, query, search_cols)

    seen = set()
    merged = []
    for idx, score in regex_results:
        if idx not in seen:
            merged.append((idx, score + 50))
            seen.add(idx)

    for idx, score in bm25_results:
        if idx not in seen and score > 0:
            merged.append((idx, score))
            seen.add(idx)

    merged.sort(key=lambda x: x[1], reverse=True)
    top_indices = [idx for idx, _ in merged[:max_results]]

    results = []
    for idx in top_indices:
        row = data[idx]
        filtered_row = {col: row.get(col, "") for col in output_cols if col in row}
        results.append(filtered_row)

    return results


def search(query, domain=None, max_results=MAX_RESULTS):
    """Main search function with auto-domain detection"""
    if domain is None:
        domain = detect_domain(query)

    config = CSV_CONFIG.get(domain, CSV_CONFIG["style"])
    filepath = DATA_DIR / config["file"]

    if not filepath.exists():
        return {"error": f"File not found: {filepath}", "domain": domain}

    results = search_domain(query, domain, max_results)

    return {
        "domain": domain,
        "query": query,
        "file": config["file"],
        "count": len(results),
        "results": results
    }


def search_stack(query, stack, max_results=MAX_RESULTS):
    """Search stack-specific guidelines"""
    config = STACK_CONFIG.get(stack)
    if not config:
        return {"error": f"Unknown stack: {stack}. Available: {', '.join(AVAILABLE_STACKS)}"}

    filepath = DATA_DIR / config["file"]
    if not filepath.exists():
        return {"error": f"Stack file not found: {filepath}", "stack": stack}

    data = load_csv(filepath)
    search_cols = config["search_cols"]
    output_cols = config["output_cols"]

    documents = []
    for row in data:
        doc_text = " ".join(str(row.get(col, "")) for col in search_cols)
        documents.append(doc_text)

    bm25 = BM25()
    bm25.fit(documents)
    bm25_results = bm25.score(query)

    regex_results = regex_search(data, query, search_cols)

    seen = set()
    merged = []
    for idx, score in regex_results:
        if idx not in seen:
            merged.append((idx, score + 50))
            seen.add(idx)

    for idx, score in bm25_results:
        if idx not in seen and score > 0:
            merged.append((idx, score))
            seen.add(idx)

    merged.sort(key=lambda x: x[1], reverse=True)
    top_indices = [idx for idx, _ in merged[:max_results]]

    results = []
    for idx in top_indices:
        row = data[idx]
        filtered_row = {col: row.get(col, "") for col in output_cols if col in row}
        results.append(filtered_row)

    return {
        "domain": "stack",
        "stack": stack,
        "query": query,
        "file": config["file"],
        "count": len(results),
        "results": results
    }
