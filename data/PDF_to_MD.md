# PDF to Markdown Cleanup

Knowledge base was created mostly by parsing pdf files of the book I helped write about Vintage Star Wars action figures. (These files are NOT included in the repo for copyright reasons)

## Clean up processes 
I used `pymupdf4llm` to convert each chapter's pdf files into mark down files but then had to perform manual clean up of each file. The book is 500 pages so this took some time.

* The ligature marks in the font the book used confused the OCR parser so any word with "fi" in it became "fi " so words like "figure" because "fi gure" and certificate became "certifi cate". Those words are heavily used in a book about Star Wars Action Figures.
* Similarlily, "fl" became "fl " so "flat became "fl at".
* The OCR of the text in the images of figure packaging was removed
* I moved around some of the stacked column elements that were layed out for humans to better understand but computer parsing was putting the data in the wrong column or making additional columns.
* Removed extra whitespace or image blocks with irrelevant OCR'ed text
* Removed page numbers and section headers/footers that were entered into the text blocks
* Moved around paragraphs that were put in the wrong order
* nested bullet points got OCR'ed into degree symbol °.  I changed them to idented bullets.
* removed headers and text pointing out parts of pictures or diagrams without any other information text
* change headers to max of 3 levels for easier chunking
* split different topics into separate md files