"""Screenshots of the "Wärmepumpe" dashboard and the heat pump's device page (Playwright, headless Chromium).

Runs inside the container mcr.microsoft.com/playwright/python (started by take_screenshots.py, --network host).
Logs in through the login form with HA_USER / HA_PASS (a temporary user) and writes PNGs to /out.
Pattern: scripts/dev/screenshot.py of the Sungrow integration repo (branch proper-ha-integration).
"""
import os
import sys

from playwright.sync_api import Page, sync_playwright

URL = "http://127.0.0.1:8123"
OUT = "/out"
DEVICE_ID = "8615f6b0d706bb7ddec9abc8575a9051"
VIEWS = ["uebersicht", "energie", "verlauf", "einstellungen", "diagnose"]


CARD_RECT = """(header) => {
    // Bounding box of the ha-card whose header property is `header` (cards sit in shadow DOM).
    let found = null;
    const walk = (root) => {
        for (const el of root.querySelectorAll('*')) {
            if (!found && el.tagName === 'HA-CARD' && el.header === header) found = el.getBoundingClientRect();
            if (el.shadowRoot) walk(el.shadowRoot);
        }
    };
    walk(document);
    return found && {x: found.x, y: found.y, width: found.width, height: found.height};
}"""
DEVICE_CARDS = ["Steuerung", "Sensoren", "Konfiguration", "Diagnose"]


def log_in(page: Page) -> None:
    page.goto(URL)
    page.locator("input[name=username]").fill(os.environ["HA_USER"])
    page.locator("input[name=password]").fill(os.environ["HA_PASS"])
    page.keyboard.press("Enter")
    page.wait_for_url(lambda now: "/auth/" not in now, timeout=30_000)
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2_000)
    # Hide the sidebar: it lists the owner's private dashboards and the user name.
    page.evaluate("localStorage.setItem('dockedSidebar', JSON.stringify('always_hidden'))")


def shoot(page: Page, path: str, name: str, wait_ms: int = 6_000, height: int = 900) -> None:
    page.set_viewport_size({"width": 1440, "height": height})
    page.goto(URL + path)
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(wait_ms)  # cards, history graphs and statistics load after networkidle
    target = f"{OUT}/{name}.png"
    page.screenshot(path=target, full_page=True)
    print("wrote", target, flush=True)


def shoot_device(page: Page) -> None:
    """The device page scrolls inside a container and is too tall for one image: top + one image per card."""
    page.set_viewport_size({"width": 1440, "height": 14000})
    page.goto(f"{URL}/config/devices/device/{DEVICE_ID}")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(6_000)
    page.screenshot(path=f"{OUT}/device-0-top.png", clip={"x": 0, "y": 0, "width": 1440, "height": 700})
    print("wrote device-0-top", flush=True)
    for i, header in enumerate(DEVICE_CARDS, 1):
        r = page.evaluate(CARD_RECT, header)
        if not r:
            print("card not found:", header, flush=True)
            continue
        target = f"{OUT}/device-{i}-{header.lower()}.png"
        page.screenshot(path=target, clip={"x": r["x"] - 8, "y": r["y"] - 8, "width": r["width"] + 16, "height": r["height"] + 16})
        print("wrote", target, round(r["height"]), flush=True)


def main() -> int:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(
            viewport={"width": 1440, "height": 900}, device_scale_factor=1, locale="de-DE",
            timezone_id="Europe/Berlin", color_scheme="light")
        page = context.new_page()
        log_in(page)
        for i, view in enumerate(VIEWS, 1):
            shoot(page, f"/dashboard-warmepumpe/{view}", f"dashboard-{i}-{view}")
        shoot_device(page)
        browser.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
