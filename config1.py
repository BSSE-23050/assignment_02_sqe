import os

# Base Edenrobe URLs
BASE_URL = 'https://edenrobe.com'
CART_PATH = '/cart'

# Main test account registered on Edenrobe using Gmail alias
TEST_EMAIL = 'chmanii803+main@gmail.com'

# Product catalog for test execution
PRODUCTS = [
    {
        'type': 'letter',
        'url': 'https://edenrobe.com/collections/men/products/full-sleeves-basic-tee-emtbf6-005',
    },
    {
        'type': 'numeric',
        'url': 'https://edenrobe.com/collections/men/products/full-sleeves-basic-tee-emtbf6-005',
    },
    {
        'type': 'age',
        'url': 'https://edenrobe.com/collections/men/products/full-sleeves-basic-tee-emtbf6-005',
    },
    {
        'type': 'none',
        'url': 'https://edenrobe.com/collections/men/products/full-sleeves-basic-tee-emtbf6-005',
    },
]

DEFAULT_PRODUCT = PRODUCTS[0]
SOLDOUT_SIZE_URL = 'https://edenrobe.com/products/mens-black-sweater-emtswt5-012?variant=52733075456273'
SOLDOUT_SIZE = 'L'

CODE_LENGTH = 6

# Email backend configuration — set to Gmail IMAP
MAIL_BACKEND = 'imap'
MAIL_USER = 'chmanii803@gmail.com'
MAIL_APP_PASSWORD = 'kpcumrcmppfvcthi'  # 16-character App Password (no spaces)

# Execution settings
PAUSE = (3, 10)
HEADLESS = False