"""
Visits the deployed Streamlit app with a real headless browser and clicks
the "wake up" button if the app is asleep. A plain HTTP request won't work
here — Streamlit Cloud needs an actual browser to establish the WebSocket
connection that starts the app.
"""

from playwright.sync_api import sync_playwright

APP_URL = "https://uk-tech-job-analyzer-ks.streamlit.app/"


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(APP_URL, wait_until="domcontentloaded", timeout=120_000)
        page.wait_for_timeout(5000)

        wake_button = page.get_by_role("button", name="Yes, get this app back up!")

        if wake_button.count() > 0:
            print("App was asleep — waking it up...")
            wake_button.click()
            page.wait_for_timeout(30_000)
            print("Done — app should be waking up now.")
        else:
            print("App is already awake. Nothing to do.")

        browser.close()


if __name__ == "__main__":
    main()