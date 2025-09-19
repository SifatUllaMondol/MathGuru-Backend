from PyPDF2 import PdfReader
import docx
import re

def extract_text_from_file(filepath):
    if filepath.endswith('.pdf'):
        reader = PdfReader(filepath)
        return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    elif filepath.endswith('.docx'):
        doc = docx.Document(filepath)
        return "\n".join([para.text for para in doc.paragraphs])
    return ""


def parse_questions(text):
        pattern = r"Q\d*:\s*(.+?)\?\s*\[([^\]]+)\]\s*Ans:\s*(.+?)(?=Q\d*:|$)"

        matches = re.findall(pattern, text, re.DOTALL)
        result = []
        for question, tags, answer in matches:
            question = question.strip()
            answer = answer.strip()
            tag_list = [tag.strip() for tag in tags.split(",")]
            result.append((question, tag_list, answer))
        return result


def calculate_type(student_class, chapter_completed):
     result = int(student_class) + int(chapter_completed)
     return result








    # pattern = r"Q\d+:\s*(.+?)\s*Ans:\s*(.+?)(?=Q\d+:|$)"
    # matches = re.findall(pattern, text, re.DOTALL)
    # return [(q.strip(), a.strip()) for q, a in matches]