import re
import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import config
from locators import L

# Safety guard: the script refuses to click anything that could pay for or confirm an order.
FORBIDDEN = ('pay now', 'complete order', 'place order', 'confirm order', 'pay ')


import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


from selenium import webdriver
from selenium.webdriver.chrome.options import Options


from selenium import webdriver
from selenium.webdriver.chrome.options import Options


import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
def dismiss_popups(d):
    """Dismisses newsletter modals, cookie overlays, or promotional popups."""
    popup_selectors = [
        "button[aria-label='Close']",
        ".modal__close",
        "button.needsclick",
        "//button[contains(@class, 'close') or text()='×']",
        "//div[contains(@class, 'modal')]//button",
    ]
    for selector in popup_selectors:
        try:
            elems = (
                d.find_elements(By.XPATH, selector)
                if selector.startswith("//")
                else d.find_elements(By.CSS_SELECTOR, selector)
            )
            for el in elems:
                if el.is_displayed():
                    d.execute_script("arguments[0].click();", el)
                    time.sleep(1)
                    return True
        except Exception:
            continue
    return False
def make_driver():
    opts = Options()
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option('useAutomationExtension', False)
    opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
    opts.add_argument("--disable-blink-features=AutomationControlled")

    # Force Selenium to use local chromedriver.exe to bypass AppData policy blocks
    driver_path = os.path.join(os.getcwd(), 'chromedriver.exe')
    service = Service(executable_path=driver_path)

    d = webdriver.Chrome(service=service, options=opts)

    d.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': '''
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        '''
    })

    d.maximize_window()
    return d


def _by(sel):
    return By.XPATH if sel.startswith('//') else By.CSS_SELECTOR


def find_any(d, sels, timeout=8):
    end = time.time() + timeout
    while True:
        for s in sels:
            try:
                for e in d.find_elements(_by(s), s):
                    if e.is_displayed():
                        return e
            except Exception:
                pass
        if time.time() >= end:
            return None
        time.sleep(0.3)


def click_any(d, sels, timeout=8):
    e = find_any(d, sels, timeout)
    if e is None:
        raise LookupError('not found: ' + str(sels[0]))
    label = (e.text or '').lower()
    if any(w in label for w in FORBIDDEN):
        raise RuntimeError('SAFETY STOP: refusing to click ' + label)
    d.execute_script('arguments[0].scrollIntoView({block:"center"})', e)
    try:
        e.click()
    except Exception:
        d.execute_script('arguments[0].click()', e)


def type_into(d, sels, value, timeout=8):
    e = find_any(d, sels, timeout)
    if e is None:
        raise LookupError('not found: ' + str(sels[0]))
    e.clear()
    if value:
        e.send_keys(value)


def tab(d):
    ActionChains(d).send_keys(Keys.TAB).perform()     # moves focus away so the field is validated


def field_value(d, sels):
    e = find_any(d, sels, timeout=2)
    return (e.get_attribute('value') or '') if e is not None else ''


def enter_code(d, code):
    # Works for one box per digit (auto-advance) and for a single box.
    box = find_any(d, L['code_boxes'], timeout=10)
    if box is None:
        raise LookupError('code boxes not found')
    box.click()
    ActionChains(d).send_keys(code).perform()


def visible(d, sels, timeout=3):
    return find_any(d, sels, timeout) is not None


def page_text(d):
    return d.find_element(By.TAG_NAME, 'body').text.lower()


def text_appears(d, words, timeout=8):
    end = time.time() + timeout
    while time.time() < end:
        t = page_text(d)
        if any(w in t for w in words):
            return True
        time.sleep(0.4)
    return False


def dismiss_popups(d):
    for s in L['popup_close']:
        try:
            for e in d.find_elements(_by(s), s):
                if e.is_displayed():
                    e.click()
                    break
        except Exception:
            pass


def uncheck_news(d):
    # The "Email me with news and offers" box is ticked by default: untick it.
    for s in L['g_news']:
        for e in d.find_elements(_by(s), s):
            if e.is_selected():
                d.execute_script('arguments[0].click()', e)


def cart_count(d):
    e = find_any(d, L['cart_count'], timeout=2)
    if e is None:
        return 0
    m = re.search(r'\d+', e.text or '')
    return int(m.group()) if m else 0


def get_rows(d):
    for s in L['cart_row']:
        rows = [r for r in d.find_elements(_by(s), s) if r.is_displayed()]
        if rows:
            return rows
    return []


def row_text(row, sels):
    for s in sels:
        els = row.find_elements(By.CSS_SELECTOR, s)
        if els:
            return (els[0].text or els[0].get_attribute('value') or '').strip()
    return ''


def select_size(d, size):
    click_any(d, [t % size for t in L['size_fmt']], timeout=5)


# ---------- size and colour: works for every product type ----------
# Edenrobe products differ: letter sizes (S to XXL), numeric sizes (42 to 46), age
# sizes (02-3y to 13-14y), a colour option (often just one colour), or nothing at all
# (perfume, unstitched dress, shawl, jewellery). Instead of one function per type,
# the script finds the SIZE: and COLOR: groups on the page and picks the first
# available choice. A group that does not exist is simply skipped.
OPTIONS_JS = """
const want = arguments[0];
const norm = e => (e.textContent || '').trim().toLowerCase().replace(/[:\\s]+$/, '');
const after = (a, b) => !!(a.compareDocumentPosition(b) & Node.DOCUMENT_POSITION_FOLLOWING);
const heads = [...document.querySelectorAll('legend,label,span,p,div,h2,h3,h4,h5,strong,b')]
  .filter(e => e.children.length === 0 && e.offsetParent !== null &&
               ['size', 'color', 'colour'].includes(norm(e)));
const h = heads.find(e => norm(e) === want || (want === 'color' && norm(e) === 'colour'));
if (!h) return [];
const next = heads.find(e => e !== h && after(h, e));
const bad = /cart|buy|checkout|guide|chart|wishlist|notify|share/i;
const maxLen = want === 'size' ? 8 : 20;
let found = [];
let box = h.parentElement;
for (let i = 0; i < 4 && box && !found.length; i++, box = box.parentElement) {
  const c = [...box.querySelectorAll('button, label, li, a, [role=radio]')].filter(e => {
    const t = (e.textContent || '').trim();
    return after(h, e) && (!next || (next.compareDocumentPosition(e) & Node.DOCUMENT_POSITION_PRECEDING)) &&
           e.offsetParent !== null && /[A-Za-z0-9]/.test(t) && t.length <= maxLen && !bad.test(t);
  });
  const leaf = c.filter(e => !c.some(o => o !== e && e.contains(o)));
  if (!leaf.length) continue;
  const p1 = leaf.filter(e => e.parentElement === leaf[0].parentElement);
  const p2 = leaf.filter(e => e.parentElement.parentElement === leaf[0].parentElement.parentElement);
  found = p1.length >= p2.length ? p1 : p2;
}
const dead = e => {
  const inp = e.control || e.querySelector('input') || e;
  const cls = ((e.className || '') + ' ' + (inp.className || '') + ' ' + (e.title || '')).toString().toLowerCase();
  const st = getComputedStyle(e);
  return !!(inp.disabled || e.disabled || e.getAttribute('aria-disabled') === 'true' ||
            /disabled|sold|unavailable|out-of-stock|soldout/.test(cls) ||
            [e, ...e.querySelectorAll('*')].some(x => getComputedStyle(x).textDecorationLine.includes('line-through')) ||
            st.pointerEvents === 'none');
};
return found.map(e => ({el: e, text: e.textContent.trim(), dead: dead(e)}));
"""


def options(d, group):
    return d.execute_script(OPTIONS_JS, group) or []


def click_el(d, e):
    d.execute_script('arguments[0].scrollIntoView({block:"center"})', e)
    try:
        e.click()
    except Exception:
        d.execute_script('arguments[0].click()', e)


def add_ready(d):
    # True when the Add to cart button is there, enabled, and not saying "sold out"
    e = find_any(d, L['add_to_cart'], timeout=2)
    return e is not None and e.is_enabled() and 'sold' not in (e.text or '').lower()


def choose_options(d):
    """Pick the first available size and colour. Returns e.g. 'size=S colour=Fawn'."""
    said = []
    sizes = options(d, 'size')
    if not sizes:
        said.append('size=none')              # perfume, unstitched dress, shawl, ...
    else:
        # available sizes first; if the page marks an unavailable size in a way the
        # script does not recognise, the Add to cart check below moves on to the next
        pick = None
        for o in [o for o in sizes if not o['dead']] + [o for o in sizes if o['dead']]:
            click_el(d, o['el'])
            time.sleep(0.5)
            if add_ready(d):
                pick = o['text']
                break
        said.append('size=%s' % (pick or 'NONE-AVAILABLE'))
    colours = options(d, 'color')
    live = [o for o in colours if not o['dead']]
    if not colours:
        said.append('colour=none')
    elif len(live) > 1:
        click_el(d, live[0]['el'])             # several colours: take the first available
        said.append('colour=%s' % live[0]['text'])
    else:
        said.append('colour=%s' % (live[0]['text'] if live else colours[0]['text']))
    return ' '.join(said)

