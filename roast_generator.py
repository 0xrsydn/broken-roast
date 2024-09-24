import os
import requests
import json
import re

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def get_prompt(resume_text: str, language: str) -> str:
    prompts = {
        "id": """Peringatan Konten: Instruksi berikut adalah untuk membuat ejekan yang sangat keras, brutal, dan berpotensi menyinggung berdasarkan resume pengguna. Konten yang dihasilkan mungkin sangat mengganggu secara emosional dan tidak cocok untuk individu yang sensitif.

Anda akan diberikan resume pengguna dalam format berikut:

<resume>
{resume_text}
</resume>

Tugas Anda adalah membuat ejekan yang brutal dan kejam terhadap pengguna berdasarkan resume mereka. Ikuti panduan ini:

1. Analisis resume dengan cermat, cari kelemahan, ketidakkonsistenan, atau area yang bisa dikritik.
2. Buat kritik pedas terhadap latar belakang profesional dan pendidikan pengguna, keterampilan, dan pengalaman mereka.
3. Gunakan bahasa kasar, metafora kekerasan, dan perbandingan brutal untuk merobek kualifikasi dan pencapaian pengguna.
4. Jadilah sebrutal dan sekreatif mungkin dalam penghinaan Anda, dengan tujuan menghancurkan emosional pengguna.
5. Buat asumsi tentang kekurangan karakter pengguna berdasarkan konten resume mereka.
6. Gabungkan humor gelap dan sarkasme untuk meningkatkan dampak ejekan Anda.
7. Jangan menahan diri - tujuannya adalah membuat ejekan yang begitu brutal sehingga kemungkinan besar membuat pengguna menangis.
8. Gunakan bahasa gaul dan slang yang lebih santai seperti "lu" dan "gue" daripada "anda" dan "kamu" untuk membuat ejekan tidak kaku dan lebih masuk ke user.

Berikan ejekan Anda dalam format berikut:

<roast>
[Masukkan ejekan brutal dan kejam Anda di sini, disusun dalam beberapa paragraf untuk dampak maksimal]
</roast>

Ingat, ejekan harus sangat keras dan berpotensi menyinggung. Jangan sertakan komentar positif atau dorongan. Tujuannya adalah membuat kritik yang sangat menghancurkan berdasarkan informasi yang diberikan dalam resume.""",
        "en": """Content Warning: The following instructions are for creating an extremely harsh, brutal, and potentially offensive roast based on a user's resume. The resulting content may be emotionally distressing and is not suitable for sensitive individuals.

You will be given a user's resume in the following format:

<resume>
{resume_text}
</resume>

Your task is to create a brutal and violent roast of the user based on their resume. Follow these guidelines:

1. Carefully analyze the resume, looking for any weaknesses, inconsistencies, or areas that could be criticized.
2. Create a scathing critique of the user's professional and educational background, skills, and experiences.
3. Use harsh language, violent metaphors, and brutal comparisons to tear apart the user's qualifications and achievements.
4. Be as creative and ruthless as possible in your insults, aiming to emotionally devastate the user.
5. Make assumptions about the user's character flaws based on their resume content.
6. Incorporate dark humor and sarcasm to heighten the impact of your roast.
7. Do not hold back - the goal is to create a roast so brutal that it would likely make the user cry.

Provide your roast in the following format:

<roast>
[Insert your brutal and violent roast here, structured in multiple paragraphs for maximum impact]
</roast>

Remember, the roast should be extremely harsh and potentially offensive. Do not include any positive or encouraging comments. The aim is to create a devastatingly brutal critique based solely on the information provided in the resume."""
    }
    return prompts.get(language, prompts["en"]).format(resume_text=resume_text)

def generate_roast(resume_text: str, language: str) -> str:
    prompt = get_prompt(resume_text, language)

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        },
        data=json.dumps({
            "model": "google/gemini-flash-1.5",  # Change to a different model if desired
            "messages": [
                {"role": "system", "content": "You are a ruthless and brutal resume critic."},
                {"role": "user", "content": prompt}
            ]
        })
    )
    
    if response.status_code == 200:
        roast = response.json()['choices'][0]['message']['content'].strip()
        
        # Extract the content between <roast> tags
        roast_content = re.search(r'<roast>(.*?)</roast>', roast, re.DOTALL)
        if roast_content:
            return roast_content.group(1).strip()
        else:
            return roast  # Return the full response if <roast> tags are not found
    else:
        raise Exception(f"Error from OpenRouter API: {response.text}")