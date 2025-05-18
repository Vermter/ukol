
import openai
import fitz


def extract_text(path):
    document = fitz.open(path)
    text = " "

    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text += page.get_text()
    return text



print(extract_text("catering.pdf"))