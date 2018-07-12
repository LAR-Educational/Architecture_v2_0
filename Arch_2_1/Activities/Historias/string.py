import re
s =  "test. vai, pota. uhsah,,"
s = re.sub(r'[^\w\s]','',s)
print s
