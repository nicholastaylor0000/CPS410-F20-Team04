from apscheduler.schedulers.blocking import BlockingScheduler
from rq import Queue
from worker import conn
from simulator import daily

q = Queue(connection=conn)
sched = BlockingScheduler()

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=16, minute=25)
def scheduled_job():
    q.enqueue(daily.task, 'http://heroku.com')

sched.start()
