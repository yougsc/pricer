import numpy as np
u=121
t=2
variable=np.sqrt(u)

while True:
    if u%t==0:
        print(t)
        break
    t=t+1
    if variable<t:
        print ("nombre premier")
        break
        