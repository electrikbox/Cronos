from crontab import CronTab
import sys


class CronHandler:
    COMMENT = "Cronos"

    def __init__(self) -> None:
        self.crons = CronTab(user=True)

    # ADD
    # =========================================================================

    def add_cron(self, received_cron):
        cmd = received_cron['command']
        schedule = " ".join([
            received_cron['minutes'],
            received_cron['hours'],
            received_cron['day_of_month'],
            received_cron['months'],
            received_cron['day_of_week'],
        ])

        if not any(
            cron.command == cmd and cron.comment == self.COMMENT
            for cron in self.crons
        ):
            new_cron = self.crons.new(command=cmd, comment=self.COMMENT)
            new_cron.setall(schedule)
            self.crons.write()
            print(f"Cron '{new_cron}' added")
        else:
            print("Cron already exist")
            sys.exit(1)


    # DELETE
    # =========================================================================
        
    def del_cron(self, cmd):
        cron_to_delete = next(
            (
                cron for cron in self.crons
                if cron.command == cmd and cron.comment == self.COMMENT
            ),
            None,
        )

        if cron_to_delete:
            self.crons.remove(cron_to_delete)
            self.crons.write()
            print(f"Cron '{cron_to_delete}' deleted")
        else:
            print("Cron not found")
            sys.exit(1)





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
