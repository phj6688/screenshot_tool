# Screenshot Tool

This tool automates the process of taking screenshots of web pages, either from a single URL or multiple URLs listed in a file. It includes features such as consent pop-up handling, element removal, and adjustable screenshot dimensions.

### Features

- Take screenshots of web pages specified by URL.
- Process multiple URLs from a file.
- Handle consent pop-ups and cookie notices.
- Remove unwanted elements from web pages before taking screenshots.
- Configure screenshot dimensions and output folder.

### Requirements

- Python 3.10+
- Playwright
- PyYAML
- Pydantic
- tqdm

### Installation

1. Ensure Python 3.10+ is installed on your system.
2. Install the required Python packages:
```bash
pip install -r reqiurements.txt
```
3. Run Playwright install command:
```bash
playwright install
```
### Configuration (Optional!)

You may want to change the output folder or add selector and cookie selectors to the appropriate fields.

```yaml
selectors:
  - '.example-selector1'
  - '.example-selector2'
cookies:
  - '#cookie-consent-button'
output_folder: 'screenshots'
```

- selectors: CSS selectors of elements to remove before taking a screenshot.
- cookies: CSS selectors of cookie consent buttons to click.
- output_folder: Folder where screenshots will be saved.

### Usage

#### Taking a Screenshot of a Single URL
```bash
python main.py --url "http://example.com"
```
#### Taking Screenshots of Multiple URLs
URLs should be listed in a text file, one URL per line. Run:

```bash
python main.py --file "urls.txt"
```
Screenshots are saved in the configured output folder, named using a combination of the URL's base and a counter.

