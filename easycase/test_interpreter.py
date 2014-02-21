# -*- coding: utf-8 -*-

import sys
from helium.api import *
 
def get_version_info_string():
    is_64_bit = sys.maxsize > 2 ** 32
    bit = "64" if is_64_bit else "32"
    major, minor, micro = sys.version_info[:3]
    return "%s bit Python version %d.%d.%d" % (
        bit, major, minor, micro
    )
 
def start_first_test_with_Helium():
    start_ie("www.baidu.com")
    write("Helium")
    press(ENTER)
    click(u'Helium_百度百科')
    mydriver = get_driver()
#     ie.close()
    kill(mydriver)
    return True
    
print "You are running %s." % get_version_info_string()
print "Status of the first test: %s" % start_first_test_with_Helium()