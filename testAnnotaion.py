# 本文件用于测试python超时注解，希望能开发出一个注解，加在一个方法上后可以使得一个方法超时后自动退出

def cost_time(period):
    import time
    print('sleeping')
    time.sleep(period)
    print('wake up')


import time


def ad(a, b):
    time.sleep(4)

    print(a + b)
    return a + b


import threading


def limit_time(f, paras):
    try:
        t = threading.Thread(target=f, args=paras)
        t.start()
        t.setDaemon(True)
        t.join(2)
    except:
        pass


def limit_time_event():
    import eventlet
    with eventlet.Timeout(3):
        ad(1, 2)


limit_time_event()
