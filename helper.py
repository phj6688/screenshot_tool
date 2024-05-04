import os
import logging
import yaml
from typing import List
from pydantic import BaseModel, Field
from playwright.sync_api import sync_playwright
from urllib.parse import urlparse
from tqdm import tqdm
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Config(BaseModel):    
    selectors: List[str]
    cookies: List[str]     
    output_folder: str
    
    @classmethod
    def load_config(cls, file_path: str):
        """Loads configuration data from a YAML file into a Config instance."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                config_data = yaml.safe_load(file)
            logging.info("Configuration loaded successfully.")
            return cls(**config_data)
            
        except yaml.YAMLError as e:
            logging.error(f"Error parsing YAML config: {e}")
            raise
        except FileNotFoundError as e:
            logging.error(f"Configuration file not found: {e}")
            raise
        except Exception as e:
            logging.error(f"Failed to load config: {e}")
            raise
        
class ScreenshotHelper:
    def __init__(self, config: Config):
        self.config = config
        
    def save_screenshot(self, screenshot_data, base_url, output_folder,counter):
        """Saves the screenshot to the specified folder."""
        os.makedirs(output_folder, exist_ok=True)
        filename = f"{counter:05d}_{base_url.replace('.', '_')}.png"
        filepath = os.path.join(output_folder, filename)
        try:
            with open(filepath, "wb") as f:
                f.write(screenshot_data)
            logging.info(f"Screenshot saved to {filepath}")
        except Exception as e:
            logging.error(f"Failed to save screenshot to {filepath}: {e}")
        
    def slow_scroll_down(self,page):
        page.evaluate("""
            async () => {
                await new Promise((resolve, reject) => {
                    var totalHeight = 0;
                    var distance = 100;
                    var timer = setInterval(() => {
                        var scrollHeight = document.body.scrollHeight;
                        window.scrollBy(0, distance);
                        totalHeight += distance;
                        if(totalHeight >= scrollHeight){
                            clearInterval(timer);
                            resolve();
                        }
                    }, 100);
                });
            }
        """)
        page.evaluate("window.scrollTo(0, 0);")

    def _handle_cookies_and_remove_selectors(self, page):
        """Handles consent pop-ups and cookie notices, and removes specified selectors."""
        # Handling cookies and consent pop-ups
        for cookie_selector in self.config.cookies:
            try:
                if page.is_visible(cookie_selector, timeout=1000):  
                    page.click(cookie_selector)
                    logging.info(f"Clicked consent button with selector: {cookie_selector}")
            except Exception as e:
                logging.warning(f"Could not click selector '{cookie_selector}': {e}")

        # Removing unwanted selectors
        for selector in self.config.selectors:
            try:
                # Remove elements by selector
                page.evaluate(f"""document.querySelectorAll('{selector}').forEach(element => element.remove());""")
                #logging.info(f"Removed elements with selector: {selector}")
            except Exception as e:
                logging.error(f"Failed to remove elements with selector '{selector}': {e}")
                
    def wait_for_content(self, page, timeout=500):
                    return page.wait_for_timeout(timeout)  
                
                

    def load_take_screenshot(self, urls: List[str], full_page: bool = True, screenshot_height: int = 2048) -> None:
        screenshot_counter = 0
        clip_region = {
                        "x": 0,
                        "y": 0,
                        "width": 1280,
                        "height": screenshot_height
                    }
        try:            
            with sync_playwright() as p:
                browser = p.firefox.launch(headless=False)
                page = browser.new_page(user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")
                for url in tqdm(urls, desc="Loading and taking screenshots...", total=len(urls)):
                    base_url_parsed = urlparse(url).netloc.lower()
                    page.goto(url, wait_until='networkidle', timeout=60000)
                    self.wait_for_content(page, 1000)
                    self._handle_cookies_and_remove_selectors(page)
                    self.slow_scroll_down(page)
                    logging.info("scroll done")
                    self.wait_for_content(page, 3000)
                    try:
                        if full_page:                         
                            screenshot_data = page.screenshot(full_page=full_page,timeout=60000)
                        else:
                            screenshot_data = page.screenshot(full_page=full_page, clip=clip_region,timeout=60000)
                        self.save_screenshot(screenshot_data, base_url_parsed, self.config.output_folder, screenshot_counter)
                        screenshot_counter += 1
                    except Exception as e:
                        logging.error(f"Error taking screenshot for {base_url_parsed}: {e}")
                browser.close()
        except Exception as e:
            logging.error(f"General error in load_take_screenshot: {e}")
            raise

        logging.info(f"Total screenshots taken: {screenshot_counter}")