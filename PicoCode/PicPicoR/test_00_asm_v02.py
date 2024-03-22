module_name = 'test_00_asm_v02.py'

import sys

print (module_name, 'starting')

@micropython.asm_thumb
def my_sum(r0, r1):
    add(r0, r0, r1)
    #  none of the reverse instructions work
    #rev(r0, r1)
    #rbit(r0, r1)
    #rev16(r0, r1)
    #revsh(r0, r1)

print (sys.byteorder)

n1 = int('100100100', 2)
print (n1)

n2 = int('000000100', 2)
print (n2)

print (module_name, 'finished')
