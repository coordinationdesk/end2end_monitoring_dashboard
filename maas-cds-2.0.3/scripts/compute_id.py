#!/usr/bin/env python3

import hashlib

# params
product_id = "c65f8c0c-9af9-11ec-a153-fa163eded267"
interface_name = "LTA_Acri"

md5 = hashlib.md5()
md5.update(product_id.encode())
md5.update(interface_name.encode())

code = md5.hexdigest()
print(code)