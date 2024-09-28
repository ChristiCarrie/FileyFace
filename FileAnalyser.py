# fileName, fileContent, webAddress

from pathlib import Path
import PyPDF2
import textrazor

textrazor.api_key = "d6c3be0ed8bfbf0dcb235a80476a8d7dd009e91a316fd21b9f939563"
client = textrazor.TextRazor(extractors=["entities", "topics", "words"])

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
    client.set_classifiers(["textrazor_iab_content_taxonomy_3.0"])
    text = client.analyze(getWordsOnlyPDF(path))
    summary = []

    for c in text.categories():
        if (c.score > 0.4):
            summary.append(c.label)

    for s in text.entities():
        if (s.confidence_score >= 5 and s.relevance_score >= 0.2):
            if (summary.count(s.matched_text.lower()) == 0):
                summary.append(s.matched_text.lower())

    for t in text.topics():
        if (t.score > 0.5):
            if (summary.count(s.matched_text.lower()) == 0):
                summary.append(s.matched_text.lower())

    for w in text.words():
        if (w.part_of_speech == "NNP" or w.part_of_speech == "NNPS"):
            if (summary.count(w.token.lower()) == 0):
                summary.append(w.token.lower())

    return summary

def webAddress():
    return

def fileAll(path):
    return fileName(path), fileExtension(path), fileContent(path)#, webAddress()
