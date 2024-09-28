# fileName, fileContent, webAddress

from pathlib import Path
import PyPDF2
import textrazor
import openai

textrazor.api_key = "d6c3be0ed8bfbf0dcb235a80476a8d7dd009e91a316fd21b9f939563"
client = textrazor.TextRazor(extractors=["entities", "topics", "words"])

openai.api_key = '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'

def fileName(path):
    filePath = Path(path)
    fileName = filePath.name
    return fileName

def fileExtension(path):
    filePath = Path(path)
    fileExtension = filePath.suffix
    return fileExtension

def getWordsOnlyPDF(path, pages):
    fE = fileExtension(path)
    if (fE != '.pdf'):
        return None
    else:
        text = ''
        with open(path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page_num in pages:
                if page_num < len(reader.pages):    
                    page = reader.pages[page_num]
                    text += page.extract_text()
                else:
                    print(f'Page {page_num} does not exist in the document.')
        return text

def summarizeFileContent(path, pages):
    features = """
    Please summarize the following text focusing on features that one would consider
    when deciding where to place it in an organized file directory. 
    For example, if the document is titled 'CS 2110 Homework 05', then it should be
    placed into a directory called 'CS 2110' or 'CS 2110/Homeworks'.
    What follows are the file name along with some text from the file.
    """
    
    prompt = f"{features}\n\nFilename: {fileName(path)}\nText:\n{getWordsOnlyPDF(path, pages)}"
    
    response = openai.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {'role': 'system', 'content': '''Your role is to summarize a pdf with the given information.'''},
            {'role': 'user', 'content': prompt}
        ],
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.5,
    )
    summary = response.choices[0].message.content
    return summary
        

# def fileContent(path):
#     client.set_classifiers(["textrazor_iab_content_taxonomy_3.0"])
#     pdfExist = getWordsOnlyPDF(path)
#     if pdfExist == None:
#         return None
#     text = client.analyze(pdfExist)
#     summary = []

#     for c in text.categories():
#         if (c.score > 0.4):
#             summary.append(c.label)

#     for s in text.entities():
#         if (s.confidence_score >= 5 and s.relevance_score >= 0.2):
#             if (summary.count(s.matched_text.lower()) == 0):
#                 summary.append(s.matched_text.lower())

#     for t in text.topics():
#         if (t.score > 0.5):
#             if (summary.count(s.matched_text.lower()) == 0):
#                 summary.append(s.matched_text.lower())

#     for w in text.words():
#         if (w.part_of_speech == "NNP" or w.part_of_speech == "NNPS"):
#             if (summary.count(w.token.lower()) == 0):
#                 summary.append(w.token.lower())

#     return summary

def webAddress():
    return

def fileAll(path):
    return fileName(path), fileExtension(path), fileContent(path)#, webAddress()