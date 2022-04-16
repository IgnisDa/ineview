import os
import threading
import time

from schedule import Scheduler

from . import models


def run_continuously(self, interval=1):
    """Continuously run, while executing pending jobs at each elapsed
    time interval.
    @returns cease_continuous_run: threading.Event which can be set to
    cease continuous run.
    Please note that it is *intended behavior that run_continuously()
    does not run missed jobs*. For example, if you've registered a job
    that should run every minute and you set a continuous run interval
    of one hour then your job won't be run 60 times at each interval but
    only once.
    """

    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                self.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.setDaemon(True)
    continuous_thread.start()
    return cease_continuous_run


Scheduler.run_continuously = run_continuously


def delete_processed_videos():
    for attempt_set in models.AttemptSet.objects.all():
        if not attempt_set.is_processed:
            continue
        for attempt in attempt_set:
            mp4_file_path = attempt.video_file.path
            webm_file_path = attempt.video_file.path.replace(".mp4", "")
            os.remove(mp4_file_path)
            os.remove(webm_file_path)
            attempt.is_purged = True
            attempt.save()


def start_scheduler():
    scheduler = Scheduler()
    scheduler.every(5).minutes.do(delete_processed_videos)
    scheduler.run_continuously()
