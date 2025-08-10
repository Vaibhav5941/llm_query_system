from django.apps import AppConfig
import os


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    def ready(self):
        from core.logic.embedder import embed_pdf_to_faiss

        pdf_path = "E:\\llm_query_system\\llm_query_system\\media\\BAJHLIP23020V012223.pdf"
        embed_pdf_to_faiss(pdf_path, pdf_id="bajaj_policy")
