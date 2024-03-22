module_name = 'test_15_A_BasicCS_v01.py'

print (module_name, 'starting')
import utime
import CommandStreamPico_V05 as CommandStream
print ('Before. in use?', CommandStream.CommandStream.in_use)
tempcs = CommandStream.CommandStream()
print ('After. in use?', CommandStream.CommandStream.in_use)
print ('After. valid?', tempcs.valid)
tempcs.send('testingg')
utime.sleep(1)
failcs = CommandStream.CommandStream()
print ('Fail. valid?', failcs.valid)
tempcs.close()
print ('Closed. in use?', CommandStream.CommandStream.in_use)
print ('Closed. valid?', tempcs.valid)
print (module_name, 'finished')
