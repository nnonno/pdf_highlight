import sys
from PyPDF2 import PdfFileWriter, PdfFileReader

from PyPDF2.generic import (
    DictionaryObject,
    NumberObject,
    FloatObject,
    NameObject,
    TextStringObject,
    ArrayObject
)

# x1, y1 starts in bottom left corner
def createHighlight(x1, y1, x2, y2, meta, color = [1, 0, 0]):
    newHighlight = DictionaryObject()

    newHighlight.update({
        NameObject("/F"): NumberObject(0),
        NameObject("/Type"): NameObject("/Annot"),
        NameObject("/Subtype"): NameObject("/Highlight"),
        NameObject("/Rect"): ArrayObject([
            FloatObject(x1),
            FloatObject(y1),
            FloatObject(x2),
            FloatObject(y2)
        ]),

        NameObject("/C"): ArrayObject([FloatObject(c) for c in color]),
        NameObject("/Rect"): ArrayObject([
            FloatObject(x1),
            FloatObject(y1),
            FloatObject(x2),
            FloatObject(y2)
        ]),
        NameObject("/QuadPoints"): ArrayObject([
            FloatObject(x1),
            FloatObject(y2),
            FloatObject(x2),
            FloatObject(y2),
            FloatObject(x1),
            FloatObject(y1),
            FloatObject(x2),
            FloatObject(y1)
        ]),
    })

    return newHighlight

def addHighlightToPage(highlight, page, output):
    highlight_ref = output._addObject(highlight);

    if "/Annots" in page:
        page[NameObject("/Annots")].append(highlight_ref)
    else:
        page[NameObject("/Annots")] = ArrayObject([highlight_ref])

def main(argv):


	pdfInput = PdfFileReader(open("test.pdf", "rb"))
	pdfOutput = PdfFileWriter()

	page1 = pdfInput.getPage(0)

	highlight = createHighlight(100, 400, 400, 500, {
	    "author": "",
	    "contents": "Bla-bla-bla"
	})

	addHighlightToPage(highlight, page1, pdfOutput)

	pdfOutput.addPage(page1)

	outputStream = open("output.pdf", "wb")
	pdfOutput.write(outputStream)


if __name__ == '__main__': sys.exit(main(sys.argv))