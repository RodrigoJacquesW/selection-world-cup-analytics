from contextlib import contextmanager

from playwright.sync_api import sync_playwright

SOFASCORE_BASE = "https://www.sofascore.com"


@contextmanager
def sofascore_browser():
    """Yield a Playwright page pre-navigated to SofaScore."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(SOFASCORE_BASE)
        try:
            yield page
        finally:
            browser.close()
