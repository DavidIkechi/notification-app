from rocketry import Rocketry
from rocketry.conds import (
    every, hourly, daily,
    after_success,
    true, false, cron
)

notification_schedule = Rocketry(config={"task_execution": "async"})
    
if __name__ == "__main__":
    # start up the rocketry script at this point
    notification_schedule.run()
    
    