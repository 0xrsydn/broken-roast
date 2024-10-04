import io
import PyPDF2
import asyncio

async def extract_text_from_pdf(file):
    def _extract():
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file))
        return "".join(page.extract_text() for page in pdf_reader.pages)
    
    return await asyncio.to_thread(_extract)
