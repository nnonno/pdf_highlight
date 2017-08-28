#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import numpy as np
# from collections import defaultdict
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTFigure, LTChar, LTComponent, LTWordBoxHorizontal, LTWordBoxVertical, LTTextLineHorizontal, LTTextLineVertical, LTAnno
from PyPDF2 import PdfFileWriter, PdfFileReader
from PyPDF2.generic import (
    DictionaryObject,
    NumberObject,
    FloatObject,
    NameObject,
    TextStringObject,
    ArrayObject
)
# from PyPDF2Highlight import createHighlight, addHighlightToPage

d=dict()
index=0


def store_word(wordBox,pageNum):
    global index 
    x = wordBox.get_text().strip()
    y = wordBox.bbox
    (a0,b0,a1,b1)=y
    if x in d.keys():
        d[x].append([pageNum,index,a0,b0,a1,b1])
        index+=1
    else:
        d[x]=[[pageNum,index,a0,b0,a1,b1]]
        index+=1

def parse_layout(layout,laparams,pageNum):
    """Function to recursively parse the layout tree."""
    for lt_obj in layout:
        if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
            parse_word(lt_obj,laparams,pageNum)
        elif isinstance(lt_obj, LTFigure):
            parse_layout(lt_obj,laparams,pageNum)  # Recursive

def parse_word(lt_obj,laparams,pageNum):

    for textline in lt_obj._objs:
        word=None
        if isinstance(textline, LTTextLineHorizontal):       
            for char in textline:
                # print char.get_text().strip()
                if isinstance(char, LTChar): 
                    x = char.get_text().strip()                  
                    if word is not None:
                        if x == '':
                            # print "WordBox(Horizontal)"
                            # print word.get_text().strip()
                            store_word(word,pageNum)
                            word = None
                        else:
                            word.add(char)
                    else:
                        if x != '':                       
                            word = LTWordBoxHorizontal()
                            word.add(char)
        word=None
        if isinstance(textline, LTTextLineVertical):       
            for char in textline:
                # print char.get_text().strip()
                if isinstance(char, LTChar): 
                    x = char.get_text().strip()                  
                    if word is not None:
                        if x == '':
                            # print "WordBox(Vertical)"
                            # print word.get_text().strip()
                            store_word(word,pageNum)
                            word = None
                        else:
                            word.add(char)
                    else:
                        if x != '':                       
                            word = LTWordBoxVertical()
                            word.add(char)

        # print textline.get_text().strip()
        # if isinstance(textline, LTTextLineHorizontal):
        #     for char in textline:
        #         # print "WordBox"
        #         temp = char.get_text().strip()
        #         # if isinstance(char, LTAnno):
        #         print(char.__class__.__name__)
        #         if temp == '':
        #             print 'none'
        #         else:
        #             print char.get_text().strip()

            # for a in char.get_text():
            #     print "%#x" % ord(a)

            # if isinstance(obj1, LTChar):
            #     print(obj1.__class__.__name__)
            #     print(obj1.get_text().strip())

    return

# x1, y1 starts in bottom left corner
def createHighlight(x1, y1, x2, y2, meta, color = [1, 0, 0]):
    newHighlight = DictionaryObject()

    newHighlight.update({
        NameObject("/F"): NumberObject(4),
        NameObject("/Type"): NameObject("/Annot"),
        NameObject("/Subtype"): NameObject("/Highlight"),

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
        # NameObject("/T"): TextStringObject(meta["author"]),
        # NameObject("/Contents"): TextStringObject(meta["contents"]),

        NameObject("/C"): ArrayObject([FloatObject(c) for c in color]),
        NameObject("/Rect"): ArrayObject([
            FloatObject(x1),
            FloatObject(y1),
            FloatObject(x2),
            FloatObject(y2)
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
    
    string=None
    file=None
    output=None
    laparams = LAParams()
    
    for opt in range(0,len(argv[1:])):
        if argv[opt] == '-s': string = argv[opt+1]
        elif argv[opt] == '-f': file = argv[opt+1]
        elif argv[opt] == '-m': output = argv[opt+1].strip()

    #
    fp = open(file, 'rb')
    parser = PDFParser(fp)
    doc = PDFDocument(parser)

    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    pageNum=0
    for page in PDFPage.create_pages(doc):
        interpreter.process_page(page)
        layout = device.get_result()
        parse_layout(layout,laparams,pageNum)
        pageNum+=1


    

    pdfInput = PdfFileReader(fp)
    pdfOutput = PdfFileWriter()
    pageNo = pdfInput.getNumPages()
    print pageNo
    for iter in range(0,pageNo):
        if iter:
            pageNew.append(pdfInput.getPage(iter))
        else:
            pageNew = [pdfInput.getPage(iter)]



    s = string.split(' ')
    indexTemp=[]
    flag=0
    for j in range(0,len(s)):
        if j:
            for i in indexTemp:
                if i[(len(i)-3)] == ' ':
                    break
                for item in d.keys():
                    if s[j] in item:
                        temp=d[item]
                        length=len(np.shape(temp))
                        for row in temp:
                            if i[2+3*(j-1)]+1==row[1]:
                                flag=1
                                i.append(item)
                                i.append(row[0])
                                i.append(row[1])
                                break
                        if flag:
                            break
                if flag == 0:
                    i.append(' ')
                    i.append(0)
                    i.append(0)
                flag = 0
        else:
            for item in d.keys():
                if s[j] in item:
                    temp=d[item]
                    for row in temp:
                        indexTemp.append([item,row[0],row[1]])
    print indexTemp
    for i in indexTemp:
        if len(i) != 3*len(s):
            break
        if i[3*(len(s)-1)] != ' ':
            result = i
            for j in range(0,len(result),3):
                for row in d[result[j]]:
                    if row[1] == result[j+2]:
                        highlight = createHighlight(row[2],row[3],row[4],row[5],{
                            "author": "",
                            "contents": ""
                        })
                        addHighlightToPage(highlight, pageNew[row[0]], pdfOutput)


    for iter in range(0,pageNo):
        pdfOutput.addPage(pageNew[iter])
    if output is None:
        output = 'output-'+file
    outputStream = open(output, "wb")
    pdfOutput.write(outputStream)
    fp.close()

    device.close()
    return

if __name__ == '__main__': sys.exit(main(sys.argv))
