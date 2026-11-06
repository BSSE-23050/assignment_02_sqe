BASE_URL = 'https://edenrobe.com'
CART_PATH = '/cart'                 # CHECK: open the cart page by hand and read the address bar

# Test account: create it by hand once and save its delivery address in the account.
# With MAIL_BACKEND = 'imap' it must be an alias of MAIL_USER, e.g. name+main@gmail.com
TEST_EMAIL = 'edenrobeqa.saqlain@mailinator.com'

# One in-stock product page for each valid product class (S-V1 to S-V4 in the report).
# Keep this order: the valid tests rotate through the list, run 1 uses the first
# product, run 2 the second, and so on. 'type' is only a label written to results.csv.
PRODUCTS = [
    # S-V1: letter sizes (S, M, L, XL, XXL), usually with one colour
    {'type': 'letter', 'url': 'https://edenrobe.com/collections/men/products/full-sleeves-basic-tee-emtbf6-005'},
    # S-V2: numeric sizes (pants, 30 to 40)
    {'type': 'numeric', 'url': 'https://edenrobe.com/collections/men-bottoms/products/mens-grey-formal-pant-embpc6-15323'},
    # S-V3: age-range sizes (kids, 02-3y to 13-14y)
    {'type': 'age', 'url': 'https://edenrobe.com/collections/sale/products/boys-navy-white-shirt-ebts5-27611'},
    # S-V4: no size and no colour (perfume, unstitched dress, shawl, jewellery)
    {'type': 'none', 'url': 'https://edenrobe.com/collections/accessories/products/cufflink-eamcl6-027'},
]
# The invalid tests (TC04, TC06, TC08) always use this product, so that a failure can
# only come from the invalid value under test and never from the product type.
DEFAULT_PRODUCT = PRODUCTS[0]

# A product that is listed, but has one size shown as unavailable (class S-I1).
# A product that is sold out in every size is removed from the site, so there is no
# "sold-out product" page to test.
SOLDOUT_SIZE_URL = 'https://edenrobe.com/collections/men-graphic-tees/products/mens-black-graphic-tee-emtgt6-001'
SOLDOUT_SIZE = ''                  # the size shown as unavailable on that page

# One-time codes
CODE_LENGTH = 6                     # CHECK: number of digits Edenrobe really sends
MAIL_BACKEND = 'mailinator'         # 'mailinator' or 'imap' (disposable Gmail)

# Only needed when MAIL_BACKEND = 'imap'
MAIL_USER = ''
MAIL_APP_PASSWORD = ''              # never put this in the report

PAUSE = (10, 20)                     # seconds between runs (assignment rule)
HEADLESS = False
