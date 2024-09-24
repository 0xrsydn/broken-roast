from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from roast_generator import generate_roast
from pdf_extractor import extract_text_from_pdf

app = FastAPI()

@app.post("/roast-resume")
async def roast_resume(file: UploadFile = File(...), language: str = Form("en")):
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