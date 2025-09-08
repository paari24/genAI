from playwright.sync_api import sync_playwright

def get_latest_match_news():
    with sync_playwright() as p:
        # Launch browser (set headless=True if you don’t want UI)
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Navigate to Google News search
        query = "India latest match"
        page.goto(f"https://news.google.com/search?q={query}")

        # Wait for news links to load
        page.wait_for_selector("a.WwrzSb")

        # Grab first 5 news links
        articles = page.locator("a.WwrzSb").all()[:5]

        if not articles:
            print("⚠ No news found. Check selectors.")
        else:
            print("Latest India Match News:")
            for i, article in enumerate(articles, start=1):
                link = article.get_attribute("href")
                if link and link.startswith("./"):  # convert relative to absolute
                    link = "https://news.google.com" + link[1:]
                print(f"{i}. {link}")

        browser.close()

if __name__ == "__main__":
    get_latest_match_news()
