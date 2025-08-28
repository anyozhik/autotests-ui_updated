from playwright.sync_api import Page, Playwright
from config import settings, Browser
from tools.playwright.mocks import mock_static_resources


def initialize_playwright_page(
        playwright: Playwright,
        test_name: str,
        browser_type: Browser,
        storage_state: str | None = None
) -> Page:
    browser = playwright[browser_type].launch(headless=settings.headless)
    context = browser.new_context(base_url=settings.get_base_url(),
                                  storage_state=storage_state)
    page = context.new_page()
    mock_static_resources(page)

    yield page
    browser.close()



