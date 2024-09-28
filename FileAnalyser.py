# fileName, fileContent, webAddress

from pathlib import Path
import PyPDF2
import textrazor

textrazor.api_key = "d6c3be0ed8bfbf0dcb235a80476a8d7dd009e91a316fd21b9f939563"
client = textrazor.TextRazor(extractors=["entities", "topics", "relations"])

def fileName(path):
    filePath = Path(path)
    fileName = filePath.name
    return fileName

def fileExtension(path):
    filePath = Path(path)
    fileExtension = filePath.suffix
    return fileExtension

def getWordsOnlyPDF(path):
    fE = fileExtension(path)
    if (fE != '.pdf'):
        return None
    else:
        with open(path, 'rb'):
            reader = PyPDF2.PdfReader(path)
            text = ''

            for i in range(len(reader.pages)):
                page = reader.pages[i]
                text += page.extract_text()
        return text
    
def fileContent(path):
    text = client.analyze(getWordsOnlyPDF(path))
    
    summary = []
    for s in text.entities():
        if (s.confidence_score >= 4 and s.relevance_score >= 0.15):
            if (summary.count(s.matched_text.lower()) == 0):
                summary.append(s.matched_text.lower())

    return summary

def webAddress():
    return

def fileAll(path):
    return fileName(path), fileExtension(path), fileContent(path), webAddress()
