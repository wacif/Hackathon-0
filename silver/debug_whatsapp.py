"""Quick debug script to inspect WhatsApp Web DOM selectors."""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

SESSION_PATH = Path(__file__).parent / "whatsapp_session"

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        str(SESSION_PATH),
        headless=False,
        args=["--no-sandbox", "--window-position=-10000,-10000", "--window-size=1280,720"],
    )
    page = browser.pages[0] if browser.pages else browser.new_page()
    print("Navigating to WhatsApp Web...")
    page.goto("https://web.whatsapp.com", timeout=60000)

    for selector in ['[data-testid="chat-list"]', '#pane-side', '[aria-label="Chat list"]']:
        try:
            page.wait_for_selector(selector, timeout=45000)
            print(f"Loaded via: {selector}")
            break
        except Exception:
            continue

    page.wait_for_timeout(5000)  # extra wait

    # Test various selectors
    tests = [
        '[role="listitem"]',
        '[role="row"]',
        '[role="option"]',
        '[aria-label*="unread"]',
        '[data-testid="cell-frame-container"]',
        '[data-testid="chat-list"] > div > div',
        '#pane-side > div > div > div',
        '#pane-side div[tabindex="-1"]',
        '#pane-side div[role="grid"] div[role="row"]',
        '#pane-side div[role="grid"] div[role="gridcell"]',
    ]

    for sel in tests:
        try:
            items = page.query_selector_all(sel)
            count = len(items)
            if count > 0:
                first_text = items[0].inner_text()[:80].replace("\n", " | ")
                print(f"  {sel} → {count} items | first: {first_text}")
            else:
                print(f"  {sel} → 0 items")
        except Exception as e:
            print(f"  {sel} → ERROR: {e}")

    # Also dump the pane-side direct children structure
    print("\n--- #pane-side structure ---")
    try:
        structure = page.evaluate("""() => {
            const pane = document.querySelector('#pane-side');
            if (!pane) return 'no #pane-side';
            function describe(el, depth) {
                if (depth > 4) return '';
                const tag = el.tagName.toLowerCase();
                const role = el.getAttribute('role') || '';
                const aria = el.getAttribute('aria-label') || '';
                const kids = el.children.length;
                const prefix = '  '.repeat(depth);
                let line = prefix + tag;
                if (role) line += ` [role=${role}]`;
                if (aria) line += ` [aria-label=${aria.substring(0,40)}]`;
                line += ` (${kids} children)`;
                let result = line + '\\n';
                if (depth < 3) {
                    for (let i = 0; i < Math.min(kids, 5); i++) {
                        result += describe(el.children[i], depth + 1);
                    }
                }
                return result;
            }
            return describe(pane, 0);
        }""")
        print(structure)
    except Exception as e:
        print(f"Error: {e}")

    browser.close()
