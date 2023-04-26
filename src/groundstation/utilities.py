import threading
import time


class PeriodicTimer:
    """
    Periodic timer can be cancelled without waiting through the cooldown
    thanks to its algorithm which is sleeping in specified periods. 
    """
    __cancel: bool = False
    
    def __init__(
            self, 
            delay: float, 
            period: float, 
            callback: callable
        ) -> None:
        
        self.delay = delay
        self.period = period
        self.callback = callback
    
    def loop(self) -> None:
        """
        Call the callback function when wait ends.
        """
        
        while self.delay > 0:
            self.delay = self.delay - self.period
            time.sleep(self.period)
            if self.__cancel:
                return
            
        self.callback()
    
    def start(self) -> None:
        """
        Start waiting.
        """
        
        self.thread = threading.Thread(target=self.loop)
        self.thread.start()
    
    def cancel(self) -> None:
        """
        Cancel the callback.
        """
        self.__cancel = True