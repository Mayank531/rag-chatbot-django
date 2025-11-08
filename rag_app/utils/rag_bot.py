import google.generativeai as genai
import base64
import os
from typing import List, Dict

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
MODEL = genai.GenerativeModel('gemini-1.5-flash')

class MultimodalRAG:
    @staticmethod
    def generate_answer(query: str, contexts: List[Dict], images: List[tuple], vector_store) -> Dict:
        # Reconstruct text context from metadata (or pass full text)
        context_text = "\n\n".join([
            f"[Page {c['metadata']['page']}] {c.get('text', '(text not stored)')}"

            for c in contexts
        ])

        relevant_images = []
        image_keywords = ["graph", "chart", "image", "figure", "table", "plot", "diagram"]
        query_lower = query.lower()
        use_images = any(k in query_lower for k in image_keywords)

        if use_images:
            pages = {c["metadata"]["page"] for c in contexts}
            for img_path, meta in images:
                if meta["page"] in pages:
                    with open(img_path, "rb") as f:
                        img_data = base64.b64encode(f.read()).decode()
                    relevant_images.append(f"data:image/png;base64,{img_data}")

        prompt = f"""
        Answer based **only** on the provided PDF context. Be concise and accurate.
        If the answer is not in context, say "I don't know."

        Question: {query}

        Context:
        {context_text}
        """

        try:
            if relevant_images:
                response = MODEL.generate_content([prompt] + relevant_images[:4])  # Limit images
            else:
                response = MODEL.generate_content(prompt)
            answer = response.text
        except Exception as e:
            answer = f"Error: {str(e)}"

        sources = [
            {"page": c["metadata"]["page"], "type": c["metadata"]["type"]}
            for c in contexts
        ]

        return {
            "answer": answer,
            "sources": sources
        }