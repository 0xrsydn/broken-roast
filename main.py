from dotenv import load_dotenv
load_dotenv()  # Add this line at the top of the file

from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.responses import JSONResponse
from roast_generator import generate_roast
from pdf_extractor import extract_text_from_pdf
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import os

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(docs_url="/ourdocs", redoc_url=None)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://cv-roast.my.id", "https://www.cv-roast.my.id", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # Add other methods as needed
    allow_headers=["*"],  # Allow all headers
)


@app.post("/roast-resume")
@limiter.limit("10/day")
async def roast_resume(request: Request, file: UploadFile = File(...), language: str = Form("en")):
    try:
        contents = await file.read()
        resume_text = await extract_text_from_pdf(contents)

        async def generate_streamed_response():
            # content_warning = "Content Warning: The following roast contains harsh content.\n"
            # yield content_warning  # Send the entire content warning as one chunk

            roast = await generate_roast(resume_text, language)

            # Yield larger chunks, like sentences or paragraphs
            for chunk in roast.split('\n'):  # Assuming `roast` is a large string
                yield chunk + '\n'  # Yield a full line or paragraph at a time
                await asyncio.sleep(0.1)  # Simulate processing delay

        return StreamingResponse(generate_streamed_response(), media_type="text/event-stream")
    
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=os.getenv("FAST_API_PORT"))
