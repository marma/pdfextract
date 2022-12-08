# PDF Extract

A simple tool for extracting text from PDFs containing swedish monographs. It attempts to filter out anything that is not deemed to be the main content, i.e static text fields that often appear in PDFs made for printing, page numbers, etc. It will also, in a minimal attempt at extracting metadata, try to find an ISBN. The ways in which information in PDFs can be laid out, hidden, obscured, etc. are numerous. Also, the structure within the PDF does not always (or often) match that of the visual layout. This means, unfortunately, that the best way to do this properly is through a visual analysis / segmentation similar to how OCR works. This is outside the scope of the tool.

Ultimately, further cleaning will be needed for some PDFs.

**TODO:** remove dependency on `pdf2txt.py`
**TODO:** better cleanup of static elements

## Installation

```
# python 3 -m venv venv
# . venv/bin/activate
# pip install -r requirements.txt
```

## Usage

```
# ./convert_pdf.sh <PDF file>
```

The output is a TSV-file with columns `id`, `ISBN` and `text`. The `id` column will **not** be consistant over multiple runs, it is simply there to lump rows from the same source together when running creating a larger file.

To run multiple PDF-files and concatenate the result do the following where `-j4` limits concurrency to four processes and `pdfs.txt` is a file with the complete path to a PDF per line. To guarantee that the ouput keeps the same order as `pdfs.txt` add the `-k` parameter.

```
# parallel -j4 ./convert_pdf.sh {}\; < pdfs.txt

```
