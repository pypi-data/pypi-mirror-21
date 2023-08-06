# Chrome-PrintToPDF

Latest Chrome Browser supports getting PDFs for websites.

## Install

Requires Python 3.5+

    pip install chrome-printtopdf


## Usage

```python
from chrome_printtopdf import get_pdf_with_chrome_sync

pdf_file = get_pdf_with_chrome_sync('http://example.org',
                                    chrome_binary='/path/to/chrome-bin')

with open('example.org.pdf', 'wb') as f:
      f.write(pdf_file.read())
```


