import os
import unittest
from crypto_aes import encrypt_gcm, decrypt_gcm, encrypt_cbc_hmac, decrypt_cbc_hmac

class TestAESRoundtrip(unittest.TestCase):
    def setUp(self):
        self.enc_key = os.urandom(32)
        self.mac_key = os.urandom(32)
        self.plain_path = "tests_plain.tmp"
        self.enc_path = "tests_enc.tmp"
        self.dec_path = "tests_dec.tmp"
        with open(self.plain_path, "wb") as f:
            f.write(b"Test payload data for AES encryption verification.")

    def tearDown(self):
        for p in [self.plain_path, self.enc_path, self.dec_path]:
            if os.path.exists(p):
                try:
                    os.remove(p)
                except OSError:
                    pass

    def test_gcm_roundtrip(self):
        encrypt_gcm(self.plain_path, self.enc_path, self.enc_key)
        decrypt_gcm(self.enc_path, self.dec_path, self.enc_key)
        with open(self.dec_path, "rb") as f:
            self.assertEqual(f.read(), b"Test payload data for AES encryption verification.")

    def test_cbc_roundtrip(self):
        encrypt_cbc_hmac(self.plain_path, self.enc_path, self.enc_key, self.mac_key)
        decrypt_cbc_hmac(self.enc_path, self.dec_path, self.enc_key, self.mac_key)
        with open(self.dec_path, "rb") as f:
            self.assertEqual(f.read(), b"Test payload data for AES encryption verification.")

if __name__ == "__main__":
    unittest.main()