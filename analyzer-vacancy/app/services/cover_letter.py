import pdfplumber
from pathlib import Path
from httpx import AsyncClient
from google import genai
from google.genai import types
from app.config import settings


class ResumeReader:
    def __init__(self):
        self.resume_path = settings.RESUME_PATH

    def read_text(self):
        resume_text = ""
        with pdfplumber.open(self.resume_path) as pdf_file:
            first_page = pdf_file.pages[0]
            table = first_page.extract_table()
            if table:
                for row in table:
                    resume_text += (
                        " | ".join(cell if cell else "" for cell in row) + "\n"
                    )

            text = first_page.extract_text()
            if text:
                resume_text += text + "\n"
        return resume_text


async def generate_cover_letter(vacancy_id: int):
    resume_reader = ResumeReader()
    resume_text = resume_reader.read_text()

    vacancy_url = f"https://api.hh.ru/vacancies/{vacancy_id}"

    async with AsyncClient(timeout=30.0) as client:
        response = await client.get(vacancy_url)
        response.raise_for_status()
        text_vacancy = response.json()

    genai_client = genai.Client(api_key=settings.GEMINI_API_KEY)

    prompt = f"""Вот вакансия - {text_vacancy}, вот мое резюме - {resume_text}
                Напиши сопроводительное письмо для работодателя данной вакансии, основываясь на моем резюме. 
                Есть ограничение - письмо должно содержать не более 110 слов"""

    response_ = genai_client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=prompt,
        config=types.GenerateContentConfig(max_output_tokens=160, temperature=0.7),
    )

    cover_letter = response_.text

    COVER_LETTERS_DIR = Path("app/cover_letters")
    COVER_LETTERS_DIR.mkdir(exist_ok=True)

    file_path = COVER_LETTERS_DIR / f"cover_letter_{vacancy_id}.txt"
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(cover_letter)

    return cover_letter
