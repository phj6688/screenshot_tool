import argparse
import logging
from typing import List
from helper import ScreenshotHelper, Config  

def read_urls_from_file(file_path: str) -> List[str]:
    """Reads URLs from a given file and returns them as a list."""
    urls = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            urls = [line.strip() for line in file.readlines() if line.strip()]
    except FileNotFoundError as e:
        logging.error(f"URL file not found: {e}")
        raise
    return urls

def main():
    # Argument parsing
    parser = argparse.ArgumentParser(description="Take screenshots of web pages.")
    parser.add_argument("-u", "--url", type=str, help="A single URL to take a screenshot of.")
    parser.add_argument("-f", "--file", type=str, help="A file path containing URLs to take screenshots of, one URL per line.")

    args = parser.parse_args()

    # Load configuration
    config = Config.load_config("config.yaml")  
    
    screenshot_helper = ScreenshotHelper(config=config)
    urls = []

    if args.url:
        urls.append(args.url)
    elif args.file:
        urls.extend(read_urls_from_file(args.file))
    else:
        parser.print_help()
        return

    if urls:
        #screenshot_helper.load_take_screenshot(urls=urls, full_page=True)
        screenshot_helper.load_take_screenshot(urls=urls, full_page=True)
    else:
        logging.error("No URLs provided.")
        parser.print_help()

if __name__ == "__main__":
    main()
