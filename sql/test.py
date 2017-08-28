from __future__ import print_function
import os
import hashlib
path = '/vagrant/p1/static/images'

files = os.listdir(path)

i = 1
a = 1

print ('INSERT INTO Photo (picid, format) values ', end = "")

while i < 30:
	if (files[i][0:7] == 'football'):
		albumid = 2
		filename = files[i]
		m = hashlib.md5(str(albumid) + filename)
		print ('(', '"', m.hexdigest(), '"', ', ', '"', files[i][-3:], '"', '), ', sep = '', end = "")

	elif (files[i][0:4] == 'space'):
		albumid = 4
		filename = files[i]
		m = hashlib.md5(str(albumid) + filename)
		print ('(', '"', m.hexdigest(), '"', ', ', '"', files[i][-3:], '"', '), ', sep = '', end = "")

	elif (files[i][0:5] == 'sports'):
		albumid = 1
		filename = files[i]
		m = hashlib.md5(str(albumid) + filename)
		print ('(', '"', m.hexdigest(), '"', ', ', '"', files[i][-3:], '"', '), ', sep = '', end = "")

	elif (files[i][0:4] == 'world'):
		albumid = 3
		filename = files[i]
		m = hashlib.md5(str(albumid) + filename)
		print ('(', '"', m.hexdigest(), '"', ', ', '"', files[i][-3:], '"', '), ', sep = '', end = "")

	i += 1

# if (files[i][0:5] == 'world'):
# 	albumid = 3
# 	filename = files[i]
# 	m = hashlib.md5(str(albumid) + filename)
# 	print ('(', '"', m.hexdigest(), '"', ', ', '"', files[i][-3:], '"', '); ', sep = '', end = "")	
