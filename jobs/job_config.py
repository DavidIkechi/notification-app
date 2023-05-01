from rocketry import Rocketry
from rocketry.conds import (
    every, hourly, daily,
    after_success,
    true, false, cron
)
from .jobs import *
import sys
sys.path.append("..")
from db.models import *

from db.session import Base, engine, Session

dbase = Session()
notification_schedule = Rocketry(
    config={"task_execution": "async"})

@notification_schedule.task("every 1 minute") 
def send_noti():
    send_notification()
    
@notification_schedule.task("every 30 seconds") 
def update_noti():
    update_notification()
    
if __name__ == "__main__":
    # start up the rocketry script at this point
    notification_schedule.run()
    
    