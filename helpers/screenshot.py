from playwright.sync_api import sync_playwright, ViewportSize
from pathlib import Path
from rich.progress import track
from utils.console import print_header, print_step, print_substep

def download_reddit_screenshots(reddit_content, number_of_screenshots):
    print_header('Downloading reddit screenshots...')

    Path("assets/screenshots").mkdir(parents=True, exist_ok=True)

    with sync_playwright() as play:
        print_step('Creating browser...')

        browser = play.chromium.launch()
        
        page = browser.new_context().new_page()
        page.goto(reddit_content['post_url'])
        page.set_viewport_size(ViewportSize(width=1920, height=1080))

        if page.locator('[data-testid="content-gate"]').is_visible():
            print_step('Content gate detected...')
            exit()

        page.locator('[data-test-id="post-content"]').screenshot(
            path="assets/screenshots/title.png")
        
        for i, comment in track(
            enumerate(reddit_content['post_comments']), 'Downloading comment screenshots..'
        ):
            if i >= number_of_screenshots:
                break
        
            if page.locator('[data-testid="content-gate"]').is_visible():
                continue

            page.goto(f'https://reddit.com{comment["comment_url"]}')
            page.locator(f'#t1_{comment["comment_id"]}').screenshot(
                path=f"assets/screenshots/comment{i}.png"
            )

        print_substep('Saved screenshots to [ assets/screenshots/ ] successfully!')
