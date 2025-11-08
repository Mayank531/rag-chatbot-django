from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Document
from .utils.pdf_processor import PDFProcessor
from .utils.vector_store import RAGVectorStore
from .utils.rag_bot import MultimodalRAG
import os
import shutil

# Global in-memory store (use Redis in production)
DOC_STORES = {}

class UploadPDFView(APIView):
    def post(self, request):
        file = request.FILES.get('pdf')
        title = request.data.get('title', file.name)

        if not file:
            return Response({"error": "No PDF provided"}, status=400)

        doc = Document.objects.create(title=title, pdf_file=file)
        pdf_path = doc.pdf_file.path
        doc_id = str(doc.id)

        # Create processing dirs
        base_dir = os.path.join('media', 'processed', doc_id)
        img_dir = os.path.join(base_dir, 'images')
        os.makedirs(img_dir, exist_ok=True)

        # Process
        processor = PDFProcessor(pdf_path, img_dir)
        text_chunks, images = processor.extract()

        # Build vector store
        vector_store = RAGVectorStore()
        vector_store.build_from_chunks(text_chunks)
        index_path = os.path.join(base_dir, 'faiss.index')
        meta_path = os.path.join(base_dir, 'metadata.pkl')
        vector_store.save(index_path, meta_path)

        # Save to global
        DOC_STORES[doc_id] = {
            "vector_store": vector_store,
            "images": images,
            "text_chunks": text_chunks,
            "index_path": index_path,
            "meta_path": meta_path
        }

        doc.faiss_index_path = index_path
        doc.processed = True
        doc.save()

        return Response({
            "doc_id": doc_id,
            "message": "PDF processed successfully"
        })

class ChatView(APIView):
    def post(self, request):
        doc_id = request.data.get('doc_id')
        query = request.data.get('query')

        if doc_id not in DOC_STORES:
            return Response({"error": "Document not found or not processed"}, status=404)

        store = DOC_STORES[doc_id]
        contexts = store["vector_store"].retrieve(query, k=3)

        # Attach actual text
        for ctx in contexts:
            page = ctx["metadata"]["page"]
            typ = ctx["metadata"]["type"]
            matches = [c for c in store["text_chunks"] if c[1]["page"] == page and c[1]["type"] == typ]
            if matches:
                ctx["text"] = matches[0][0][:1000]  # limit

        result = MultimodalRAG.generate_answer(
            query, contexts, store["images"], store["vector_store"]
        )

        return Response(result)