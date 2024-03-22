module_name = 'test_00_B_files_v02.py'

print (module_name, 'starting')

logfile = open('../test_00_B_files_log.txt','w')
logfile.write('testing 01\n')
logfile.write('testing 02\n')
logfile.close()

print (module_name, 'finished')
