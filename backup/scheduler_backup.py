from apscheduler.schedulers.background import BackgroundScheduler


class SchedulerBackup:
    def __init__(self, gestore_backup):
        self.gestore_backup = gestore_backup
        self.scheduler = BackgroundScheduler()

    def avvia_background(self):
        """
        Pianifica il backup ogni giorno alle 23:00 in background.
        """
        self.scheduler.add_job(self.gestore_backup.effettuaBackup, "cron", hour=23, minute=0)
        self.scheduler.start()
        print("🔄 Scheduler avviato in background: backup ogni giorno alle 23:00")