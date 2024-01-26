
# DELETE
# =========================================================================

def del_cron(self, cron_to_delete):

    self.crons.remove(cron_to_delete)
    self.crons.write()
    print(f"Cron '{cron_to_delete}' removed")

# PAUSE
# =========================================================================

def pause_cron(self, cron_to_pause):
    schedule, cmd = self.remote_cron_json_to_str(cron_to_pause)
    cron_to_check = f"{schedule} {cmd} # {self.COMMENT}"
    cron_test = self.crons.find_command(cmd)

    for cron_t in cron_test:
        print(f"{cron_t} : {type(cron_t)}")

    self.crons.write()
    print(f"Cron '{cron_to_pause}' paused")
