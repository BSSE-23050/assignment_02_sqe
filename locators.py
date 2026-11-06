def xp(text):
    # case-insensitive "contains text" XPath for buttons and links
    low = 'abcdefghijklmnopqrstuvwxyz'
    return ('//*[self::button or self::a][contains(translate(normalize-space(.), "%s", "%s"), "%s")]'
            % (low.upper(), low, text.lower()))


# Every entry is a list of fallbacks; the first visible match wins.
# Entries starting with // are XPath, all others are CSS selectors.
L = {
    'popup_close':  ['button[aria-label*="lose" i]', xp('no thanks')],
    'account_icon': ['a[href*="/account"]', 'a[aria-label*="account" i]', 'button[aria-label*="account" i]'],
    'auth_email':   ['input[type=email]', 'input[name*=email]', 'input[autocomplete=email]'],
    'auth_continue': [xp('continue'), xp('send code'), xp('sign in'), xp('next'), 'form button[type=submit]'],
    'code_boxes':   ['input[autocomplete=one-time-code]', 'input[inputmode=numeric]', 'input[maxlength="1"]'],
    'logged_in':    ['a[href*=logout]', xp('log out'), xp('sign out')],   # CHECK: what shows you are logged in
    'error':        ['[role=alert]', '[class*=error]', '[class*=invalid]'],
    'size_fmt':     ['//label[normalize-space(.)="%s"]', '//button[normalize-space(.)="%s"]',
                     '//li[normalize-space(.)="%s"]'],
    'add_to_cart':  [xp('add to cart'), 'button[name=add]', 'button[id*=AddToCart]',
                     'button[class*=add-to-cart]', 'form[action*="/cart/add"] button[type=submit]'],
    'close_drawer': ['button[aria-label*="close" i]', '[class*=drawer] [class*=close]', xp('close')],
    'cart_count':   ['#cart-icon-bubble', '.cart-count-bubble', '[class*=cart-count]', '[class*=cart-bubble]'],
    'cart_row':     ['tr.cart-item', '.cart-item', 'li[class*=cart-item]'],
    'row_name':     ['a[href*="/products/"]', '[class*=name]', '[class*=title]'],
    'row_qty':      ['input[type=number]', '[class*=quantity] input'],
    'row_price':    ['[class*=price]'],
    'row_variant':  ['[class*=variant]', '[class*=option]', '[class*=property]', 'dl', '[class*=meta]'],
    'checkout_btn': [xp('check out'), xp('checkout'), 'button[name=checkout]', 'a[href*=checkout]'],
    # guest checkout form
    'g_email':      ['#email', 'input[type=email]', 'input[autocomplete=email]'],
    'g_first':      ['input[name=firstName]', 'input[autocomplete=given-name]'],
    'g_last':       ['input[name=lastName]', 'input[autocomplete=family-name]'],
    'g_address':    ['input[name=address1]', 'input[autocomplete=address-line1]', 'input[placeholder*="complete address" i]'],
    'g_landmark':   ['input[name=address2]', 'input[placeholder*="landmark" i]'],
    'g_city':       ['input[name=city]', 'input[autocomplete=address-level2]'],
    'g_postal':     ['input[name=postalCode]', 'input[autocomplete=postal-code]'],
    'g_phone':      ['input[name=phone]', 'input[type=tel]'],
    'g_news':       ['#marketing_opt_in'],
    'shipping_option': ['input[type=radio][name*=shipping]', 'input[type=radio][name*=delivery]',
                        '[class*=shipping] input[type=radio]'],
}