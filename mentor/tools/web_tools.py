from duckduckgo_search import DDGS
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup


def web_search(query: str, max_results: int = 5) -> list[dict]:
    """
    Perform a free web search using DuckDuckGo.
    
    Returns a list of dicts: [{"title": ..., "href": ..., "body": ...}]
    """
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
        return results
    except Exception as e:
        return [{"error": f"Search failed: {e}"}]


def scrape_web_page(url: str) -> str:
    """
    Render a webpage using headless Playwright Chromium and extract clean text.
    
    Strips script, style, nav, and footer tags, returning up to 4000 characters.
    """
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, wait_until="domcontentloaded", timeout=15000)
            html_content = page.content()
            browser.close()

        soup = BeautifulSoup(html_content, "html.parser")

        # Strip clutter tags
        for element in soup(["script", "style", "nav", "footer", "header", "aside"]):
            element.extract()

        text = soup.get_text(separator="\n", strip=True)
        return text[:4000]
    except Exception as e:
        return f"Error scraping URL {url}: {e}"
