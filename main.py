from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from roast_generator import generate_roast
from pdf_extractor import extract_text_from_pdf
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.post("/roast-resume")
@limiter.limit("6/day")
async def roast_resume(request: Request, file: UploadFile = File(...), language: str = Form("en")):
    try:
        contents = await file.read()
        resume_text = extract_text_from_pdf(contents)
        roast = generate_roast(resume_text, language)
        
        content_warning = "Content Warning: The following roast contains extremely harsh, brutal, and potentially offensive content. It is not suitable for sensitive individuals and may be emotionally distressing."
        
        return JSONResponse(content={
            "content_warning": content_warning,
            "roast": roast
        }, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)