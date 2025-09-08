from playwright.sync_api import sync_playwright

def scrape_facebook_metadata():
    with sync_playwright() as p:
        # Launch browser (headless=True so no UI opens)
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Open Facebook homepage
        page.goto("https://www.facebook.com", timeout=60000)

        # Grab all <meta> elements
        meta_elements = page.locator("meta").all()

        # Collect metadata
        lines = []
        for meta in meta_elements:
            name = meta.get_attribute("name")
            prop = meta.get_attribute("property")
            content = meta.get_attribute("content")

            line = f"name={name}, property={prop}, content={content}"
            lines.append(line)

        # Save to text file
        with open("facebook_metadata.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        print("✅ Metadata saved to facebook_metadata.txt")

        browser.close()

if __name__ == "__main__":
    scrape_facebook_metadata()
