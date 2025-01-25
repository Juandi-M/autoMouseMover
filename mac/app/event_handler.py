# event_handler.py
import logging
from typing import Callable, Optional
import objc
from Foundation import NSObject, NSRunLoop, NSDate
from AppKit import NSWorkspace, NSWorkspaceWillSleepNotification, NSWorkspaceDidWakeNotification

class SystemEventHandler(NSObject):
    def init(self):
        self = objc.super(SystemEventHandler, self).init()
        if self is None: return None
        
        self.sleep_callback: Optional[Callable] = None
        self.wake_callback: Optional[Callable] = None
        
        # Register for sleep/wake notifications
        ws = NSWorkspace.sharedWorkspace()
        nc = ws.notificationCenter()
        
        nc.addObserver_selector_name_object_(
            self,
            self.willSleep_,
            NSWorkspaceWillSleepNotification,
            None
        )
        
        nc.addObserver_selector_name_object_(
            self,
            self.didWake_,
            NSWorkspaceDidWakeNotification,
            None
        )
        
        return self
        
    def willSleep_(self, notification):
        logging.info("System is going to sleep")
        if self.sleep_callback:
            self.sleep_callback()
            
    def didWake_(self, notification):
        logging.info("System did wake up")
        if self.wake_callback:
            self.wake_callback()
            
    def set_callbacks(self, sleep_callback: Callable, wake_callback: Callable):
        self.sleep_callback = sleep_callback
        self.wake_callback = wake_callback

class AppEventHandler:
    def __init__(self, app):
        self.app = app
        self.system_handler = SystemEventHandler.alloc().init()
        self.setup_handlers()
        
    def setup_handlers(self):
        self.system_handler.set_callbacks(
            self.handle_sleep,
            self.handle_wake
        )
        
    def handle_sleep(self):
        """Handle system sleep event"""
        logging.info("Handling sleep event")
        self.app.handle_system_sleep()
        
    def handle_wake(self):
        """Handle system wake event"""
        logging.info("Handling wake event")
        self.app.handle_system_wake()
        
    def handle_minimize(self):
        """Handle window minimize event"""
        logging.info("Handling minimize event")
        self.app.handle_minimize()
        
    def handle_restore(self):
        """Handle window restore event"""
        logging.info("Handling restore event")
        self.app.handle_restore()