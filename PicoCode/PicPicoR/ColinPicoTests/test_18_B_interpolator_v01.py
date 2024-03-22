import RemoteControl_v14 as RemoteControl

print ('Testing Interpolator')
keys = [50, 60, 62, 100]
values = [-1.0, 0.0, 0.0, 1.0]
print (keys)
print (values)
dummy_interpolator2 = RemoteControl.Interpolator('dummy2', keys, values)
for key in [45,50,55,60,61,61.9,65,70,75,80,100,105]:
    print (key, dummy_interpolator2.interpolate(key))

