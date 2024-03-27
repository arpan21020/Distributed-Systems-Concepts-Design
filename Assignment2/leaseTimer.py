import time
import threading


class ThreadTimer:
    def __init__(self, timeout, callback):
        self.timeout = timeout
        self.callback = callback
        self.timer = None
        self.start_time = None

    def start(self):
        try:
            self.start_time = time.time()
            self.timer = threading.Timer(self.timeout, self.callback)
            self.timer.start()
        except:
            # print("ERROR: in starting the timer")  
            exit(1)  

    def cancel(self):
        if self.timer:
            self.timer.cancel()
            self.timer = None
            
    def is_alive(self):
        if self.timer:
            return self.timer.is_alive()
        return False
    
    def remaining(self):
        if not self.start_time:
            return None
        elapsed = time.time() - self.start_time
        remaining = self.timeout - elapsed
        return max(0, remaining)
    
    def renew_leader_lease(self):
        # Renew the lease here...
        if self.timer is not None:
            self.timer.cancel() 
        # Then reinitialize the timer
        self.timer = ThreadTimer(self.timeout, self.renew_leader_lease)
        self.timer.start()

    def update_leader_lease(self,updated_value):
        # Renew the lease here...
        if self.timer is not None:
            self.timer.cancel()

        # Then reinitialize the timer
        self.timer = ThreadTimer(updated_value, self.cancel)
        self.timer.start()
    def restart(self):
        try:
            self.cancel()
            self.start()
        except: 
            # print("ERROR: in restarting the timer")   
            exit(1) 
    def void(self):
        return

# Usage:
# timer = LeaseTimer(5.0, callback)
# timer.start()
# print(timer.remaining())
