import allure
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
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    page = context.new_page()
    mock_static_resources(page)

    yield page

    context.tracing.stop(path=settings.tracing_dir.joinpath(f'{test_name}.zip'))
    browser.close()

    allure.attach.file(settings.tracing_dir.joinpath(f'{test_name}.zip'), name='trace', extension='zip')

