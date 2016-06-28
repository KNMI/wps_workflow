# python
from sys import argv
import serve_netcdf

scripts, combo_url, url1 , url2 = argv


print "start"

print combo_url
print url1
print url2

serve_netcdf.visualise(url1,url2,combo_url)

print "end"