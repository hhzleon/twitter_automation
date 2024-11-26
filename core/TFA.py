import pyotp

def getTwoFa(base32code):
    twoFa = pyotp.TOTP(base32code)
    return twoFa.now()