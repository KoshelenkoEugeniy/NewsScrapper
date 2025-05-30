from logic.scraper import extract_article
from logic.genai import summarize_and_extract_topics
from logic.semantic_store import store_document, semantic_search

def handle_generate_summary(url, output_box):
    try:
        article = extract_article(url)
        if not article:
            output_box.insert("end", "❌ Can't parse article.\n")
            return

        result = summarize_and_extract_topics(article['content'])
        summary = result.get("summary", "")
        topics = result.get("topics", [])

        store_document(url, summary, topics, article['content'])

        output = f"\nSummary:\n{summary}\n\nTopics:\n{', '.join(topics)}"
        output_box.insert("end", output)
    except Exception as e:
        output_box.insert("end", f"Error: {e}\n")

def handle_search(query, output_box):
    try:
        results = semantic_search(query)
        if results is None:
            output_box.insert("end", "🔍 No documents have been saved yet. Try summarizing an article first.\n")
            return
        if not results:
            output_box.insert("end", "No relevant results found.\n")
            return

        for i, res in enumerate(results, 1):
            output_box.insert("end", f"\n\n*** Result {i}: ***\n\n{res.page_content}\n")
    except Exception as e:
        output_box.insert("end", f"Error: {e}\n")