import email
import imaplib
import random
import re
import time
import config


def new_email():
    """A fresh address for every run, so a registration never hits a used one."""
    stamp = '%d%03d' % (time.time(), random.randint(0, 999))
    if config.MAIL_BACKEND == 'imap':
        name, domain = config.MAIL_USER.split('@')
        return '%s+qa%s@%s' % (name, stamp, domain)
    return 'edenrobeqa.%s@mailinator.com' % stamp


def _find_code(text):
    m = re.search(r'(?<!\d)(\d{%d})(?!\d)' % config.CODE_LENGTH, text)
    return m.group(1) if m else None


def _imap_code(address, timeout):
    end = time.time() + timeout
    while time.time() < end:
        box = imaplib.IMAP4_SSL('imap.gmail.com')
        try:
            box.login(config.MAIL_USER, config.MAIL_APP_PASSWORD)
            box.select('INBOX')
            
            # Search for all unseen messages, fallback to all messages if unseen is empty
            _, ids = box.search(None, 'UNSEEN')
            if not ids[0]:
                _, ids = box.search(None, 'ALL')
                
            for num in reversed(ids[0].split()[-5:]):  # inspect the 5 newest messages
                _, data = box.fetch(num, '(RFC822)')
                msg = email.message_from_bytes(data[0][1])
                
                body = ''
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() in ('text/plain', 'text/html'):
                            body += part.get_payload(decode=True).decode(errors='ignore')
                else:
                    body = msg.get_payload(decode=True).decode(errors='ignore')
                    
                code = _find_code(re.sub(r'<[^>]+>', ' ', body))
                if code:
                    return code
        except Exception:
            pass
        finally:
            try:
                box.logout()
            except Exception:
                pass
        time.sleep(4)
    return None

def _mailinator_code(address, timeout):
    from selenium import webdriver
    from selenium.webdriver.common.by import By

    inbox = address.split('@')[0]

    opts = webdriver.ChromeOptions()
    if config.HEADLESS:
        opts.add_argument('--headless=new')
    d = webdriver.Chrome(options=opts)

    try:
        d.get('https://www.mailinator.com/v4/public/inboxes.jsp?to=' + inbox)
        end = time.time() + timeout

        while time.time() < end:
            # Look for non-empty email rows in the inbox table
            rows = [
                r
                for r in d.find_elements(
                    By.CSS_SELECTOR,
                    'tr[aria-label*="Received"], tr.ng-scope, tbody tr',
                )
                if r.is_displayed() and r.text.strip()
            ]

            if rows:
                rows[0].click()  # Open latest email
                time.sleep(3)

                # Check main body text directly first
                body_text = d.find_element(By.TAG_NAME, 'body').text
                code = _find_code(body_text)
                if code:
                    return code

                # Switch into Mailinator's message body iframe
                frames = d.find_elements(
                    By.CSS_SELECTOR,
                    'iframe#html_msg_body, iframe#texthtml_msg_body, iframe',
                )
                for frame in frames:
                    try:
                        d.switch_to.frame(frame)
                        frame_text = d.find_element(By.TAG_NAME, 'body').text
                        code = _find_code(frame_text)
                        d.switch_to.default_content()
                        if code:
                            return code
                    except Exception:
                        d.switch_to.default_content()

            time.sleep(4)
            d.refresh()

        return None
    finally:
        d.quit()


def get_code(address, timeout=180):
    if config.MAIL_BACKEND == 'imap':
        code = _imap_code(address, timeout)
    else:
        code = _mailinator_code(address, timeout)
    if code:
        with open('last_code.txt', 'w') as f:  # remembered for the stale-code class
            f.write(code)
    return code


def stale_code():
    try:
        with open('last_code.txt') as f:
            return f.read().strip() or None
    except OSError:
        return None