import sys
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTFigure
from PyPDF2 import PdfFileWriter, PdfFileReader

# from PyPDF2Highlight import createHighlight, addHighlightToPage

d={}
index=0

def parse_layout(layout):
    """Function to recursively parse the layout tree."""
    global index 
    for lt_obj in layout:
        print(lt_obj.__class__.__name__)
        print(lt_obj.bbox)
        if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
            print(lt_obj.get_text())
            d[lt_obj.get_text().strip()]=(index,lt_obj.bbox)
            index+=1
        elif isinstance(lt_obj, LTFigure):
            parse_layout(lt_obj)  # Recursive

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
        NameObject("/F"): NumberObject(4),
        NameObject("/Type"): NameObject("/Annot"),
        NameObject("/Subtype"): NameObject("/Highlight"),

        NameObject("/T"): TextStringObject(meta["author"]),
        NameObject("/Contents"): TextStringObject(meta["contents"]),

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
    
    fp = open(argv[1], 'rb')
    [s]=argv[2:]

    parser = PDFParser(fp)
    doc = PDFDocument(parser)

    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.create_pages(doc):
        interpreter.process_page(page)
        layout = device.get_result()
        parse_layout(layout)
    # for i in sentence
    #     d.get(i,None)[0]
    # print d
    # print d.get('W o r l d', 0.0)
    # print s
    # print argv[1]
    pdfInput = PdfFileReader(open(argv[1], 'rb'))
    pdfOutput = PdfFileWriter()

    page1 = pdfInput.getPage(0)
    print s
    s=s.lower()
    for item in d.keys():
        if s in item.lower():
            (x1,y1,x2,y2)=d[item][1]
            highlight = createHighlight(x1,y1,x2,y2,{
                "author": "",
                "contents": ""
            })
            addHighlightToPage(highlight, page1, pdfOutput)
            print 'found the sentence!'

    pdfOutput.addPage(page1)

    outputStream = open("output.pdf", "wb")
    pdfOutput.write(outputStream)


if __name__ == '__main__': sys.exit(main(sys.argv))