from django.contrib.auth.hashers import (
    PBKDF2PasswordHasher, SHA1PasswordHasher, BCryptSHA256PasswordHasher, check_password, make_password
)



from django.conf import settings
from django.contrib.auth.password_validation import validate_password


class PBKDF2WrappedSHA1PasswordHasher(PBKDF2PasswordHasher):
    algorithm = 'pbkdf2_wrapped_sha1'

    def encode_sha1_hash(self, sha1_hash, salt, iterations=None):
        return super(PBKDF2WrappedSHA1PasswordHasher, self).encode(sha1_hash, salt, iterations)

    def encode(self, password, salt, iterations=None):
        _, _, sha1_hash = SHA1PasswordHasher().encode(password, salt).split('$', 2)
        return self.encode_sha1_hash(sha1_hash, salt, iterations)


a = check_password('12345abc', 'pbkdf2_sha256$36000$EWc8tdNd0Osa$z7hL7mmz8n0DUt2RtCUnO0of0OZczPI8NWhP8VQqkV0=')


b = make_password('maidiep')

c = validate_password('12345abcdsfesf')
print(c)