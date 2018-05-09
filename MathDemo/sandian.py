import matplotlib.pyplot as plt
import numpy as np

from time import sleep
from functools import wraps
import logging
logging.basicConfig()
log = logging.getLogger("retry")

def retry(f):
    @wraps(f)
    def wrapped_f(*args, **kwargs):
        MAX_ATTEMPTS = 5
        for attempt in range(1, MAX_ATTEMPTS + 1):
            try:
                return f(*args, **kwargs)
            except:
                log.exception("Attempt %s/%s failed : %s",
                        attempt,
                        MAX_ATTEMPTS,
                        (args, kwargs))
                sleep(10 * attempt)
                log.critical("All %s attempts failed : %s",
                        MAX_ATTEMPTS,
                        (args, kwargs))
    return wrapped_f


counter = 0
@retry
def testetry():
    global  counter

    counter += 1
    print(counter)
    if counter < 2:
        print("失败",counter)
        raise ValueError()
    print("调用",counter)

try:
    testetry()
except:
    print("失败", counter)

y= np.random.standard_normal((600,2))
plt.figure(figsize=(8, 5))
c=np.random.randint(0,10,len(y))
plt.scatter(y[:,0],y[:,1],c=c, marker= 'o')
plt.colorbar()
plt.grid(True)
plt.xlabel('1st')
plt.ylabel('2nd')
plt.title('Scatter Plot')
plt.show()
