# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
import magic
# Create your tests here.
mime = magic.Magic(mime=True)
print(mime.from_file("static/image/ava.png"))

from bcrypt import hashpw, gensalt
hashed = hashpw("123456".encode('utf8'), gensalt())
print (hashed)