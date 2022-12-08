# PDF Extract

A tool for extracting text from PDFs containing swedish monographs. It attempts to filter out anything that is not deemed to be the main content, i.e static text fields that often appear in PDFs made for printing, page numbers, etc. It will also, in a minimal attempt at extracting metadata, try to find an ISBN. The ways in which information in PDFs can be laid out, hidden, obscured, etc. are numerous. Also, the structure within the PDF does not always (or often) match that of the visual layout. This means, unfortunately, that the best way to do this properly is through a visual analysis / segmentation similar to how OCR works. This is outside the scope of this tool.

Ultimately, further cleaning will be needed for some PDFs.

## Usage

```
# pdf_to_text.sh <PDF file> | ./dehyphenate.py | ./text_to_tsv.py
```
