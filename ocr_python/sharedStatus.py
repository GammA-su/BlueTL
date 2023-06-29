# sharedStatus.py
import threading

class SharedStatus:
    def __init__(self):
        self.lock = threading.Lock()
        self.condition = threading.Condition(lock=self.lock)
        self.status = {
            "ready": False,
            "first_update_done": False
        }

    def set_ready(self, value):
        with self.lock:
            self.status["ready"] = value

            if value:
                self.status['first_update_done'] = True
                self.condition.notify_all()

    def wait_first_update(self):
        with self.lock:
            while not self.status["first_update_done"]:
                self.condition.wait()

# Create a global instance of the SharedStatus class
sharedStatus = SharedStatus()