import config

N = config.CODE_LENGTH

# Each invalid class is (class id, kind or field, value). The ids match the
# equivalence class tables in the report, and are written to results.csv.

UC1_EMAIL = [
    ('E-I1', 'email', ''),
    ('E-I2', 'email', 'edenrobeqa.test.com'),
    ('E-I3', 'email', 'edenrobeqa@@mailinator.com'),
    ('E-I4', 'email', '@mailinator.com'),
    ('E-I5', 'email', 'edenrobeqa@'),
    ('E-I6', 'email', 'edenrobeqa@mailinator'),
    ('E-I7', 'email', 'edenrobe qa@mailinator.com'),
    ('E-I8', 'email', 'a' * 70 + '@mailinator.com'),
]
UC2_EMAIL = [
    ('E-I1', 'email', ''),
    ('E-I2', 'email', 'nouser.com'),
    ('E-I3', 'email', 'nouser@'),
    ('E-I4', 'email', 'no user@mailinator.com'),
]
CODES = [
    ('C-I1', 'incomplete', '123'),
    ('C-I2', 'wrong', '0' * N),
    ('C-I3', 'stale', 'STALE'),
]

GUEST_ORDER = ['email', 'first', 'last', 'address', 'landmark', 'city', 'postal', 'phone']
GUEST_VALID = {
    'email': 'guest.qa@mailinator.com', 'first': 'Ayesha', 'last': 'Khan',
    'address': 'House 1, Street 2, Sector F-10', 'landmark': 'Near Main Market',
    'city': 'Islamabad', 'postal': '44000', 'phone': '03001234567',
}
GUEST = [
    ('G-E1', 'email', ''), ('G-E2', 'email', 'guest.qa.com'),
    ('G-E3', 'email', 'guest.qa@'), ('G-E4', 'email', 'guest qa@mailinator.com'),
    ('G-F1', 'first', ''), ('G-F2', 'first', '12345'), ('G-F3', 'first', '@#$%&'),
    ('G-F4', 'first', 'Ayesha123'), ('G-F5', 'first', 'a' * 60),
    ('G-L1', 'last', ''), ('G-L2', 'last', '12345'), ('G-L3', 'last', '@#$%&'),
    ('G-L4', 'last', 'Khan123'), ('G-L5', 'last', 'a' * 60),
    ('G-A1', 'address', ''), ('G-A2', 'address', '   '), ('G-A3', 'address', '@@@###'),
    ('G-M1', 'landmark', ''), ('G-M2', 'landmark', '@@@###'),
    ('G-C1', 'city', ''), ('G-C2', 'city', '12345'), ('G-C3', 'city', '@#$%&'),
    ('G-P1', 'postal', 'abcde'), ('G-P2', 'postal', '4400044000440004'),
    ('G-H1', 'phone', ''), ('G-H2', 'phone', 'abcdefghijk'), ('G-H3', 'phone', '0300123'),
    ('G-H4', 'phone', '030012345678901234'), ('G-H5', 'phone', '@#$%^&*()!'),
]
# "Too long" classes: the site may cut the text instead of showing an error.
LONG_IDS = {'G-F5', 'G-L5', 'G-P2', 'G-H4'}

CART = [
    ('K-I1', 'cart', ''), ('Q-I1', 'qty', '0'), ('Q-I2', 'qty', '999'),
    ('Q-I3', 'qty', '-1'), ('Q-I4', 'qty', 'abc'),
]
CONTINUE = [
    ('S-I1', 'size', ''),      # unavailable size on the first item
]

# Invalid test cases only. Valid test cases (TC01, TC03, ...) have no entry.
CLASSES = {
    'TC02': UC1_EMAIL + CODES,
    'TC04': UC2_EMAIL + CODES + [('S-I1', 'soldout', '')],
    'TC06': GUEST,
    'TC08': CART,
    'TC10': CONTINUE,
}
