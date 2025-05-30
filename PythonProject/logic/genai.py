from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_and_extract_topics(article_text):
    prompt = f"""
    Summarize the following article and extract 3-5 main topics.
    Return in this format:
    Summary: <summary text>
    Topics: <comma-separated list>

    Article:
    {article_text}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )

    content = response.choices[0].message.content.strip()
    summary = ""
    topics = []

    if "Summary:" in content and "Topics:" in content:
        summary_part = content.split("Summary:")[1].split("Topics:")[0].strip()
        topics_part = content.split("Topics:")[1].strip()
        summary = summary_part
        topics = [t.strip() for t in topics_part.split(",") if t.strip()]

    return {"summary": summary, "topics": topics}