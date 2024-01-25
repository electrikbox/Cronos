from crontab import CronTab
import sys


class CronHandler:
    COMMENT = "Cronos"

    def __init__(self) -> None:
        self.crons = CronTab(user=True)

    # GET all local crons
    # =========================================================================

    @staticmethod
    def get_local_crons():
        crons = CronTab(user=True)
        return crons

    # Cron to string
    # =========================================================================

    def cron_to_str(self, cron: dict):
        cmd = cron['command']
        schedule = " ".join([
            cron['minutes'],
            cron['hours'],
            cron['day_of_month'],
            cron['months'],
            cron['day_of_week'],
        ])
        return (schedule, cmd)

    # ADD
    # =========================================================================

    def add_cron(self, received_cron):

        schedule, cmd = self.cron_to_str(received_cron)
        cron_to_check = f"{schedule} {cmd} # {self.COMMENT}"

        if not any(str(cron) == cron_to_check for cron in self.crons):
            new_cron = self.crons.new(command=cmd, comment=self.COMMENT)
            new_cron.setall(schedule)
            self.crons.write()
            print(f"Cron '{new_cron}' added")
        else:
            print(f"Cron ({schedule} {cmd}) already exist")

    # DELETE
    # =========================================================================

    def del_cron(self, cron_to_delete):

        self.crons.remove(cron_to_delete)
        self.crons.write()
        print(f"Cron '{cron_to_delete}' removed")


if __name__ == "__main__":

    RECEIVED_CRON = {
        'minutes': '0',
        'hours': '10',
        'day_of_month': '22',
        'months': 'jul',
        'day_of_week': '*',
        'command': 'pwd',
        'user': 1,
        'is_paused': False,
        'validated': False
    }

    my_crons = CronHandler()
    # my_crons.add_cron(RECEIVED_CRON)
    # my_crons.del_cron("pwd")
