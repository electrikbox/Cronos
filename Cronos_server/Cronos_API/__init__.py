# Crons create api url
# =============================================================================

CRON_CREATE_API_URL = "http://localhost:8000/api/crons/create/"
CRON_LIST_API_URL = "http://localhost:8000/api/crons/"
LOGS_LIST_API_URL = "http://localhost:8000/api/logs/"


# Time
# =============================================================================

TIME_ALLOWED_MSG = "Only time from 00:00 to 23:59."

# Minutes
# =============================================================================

MINUTES_RANGE = [str(i) for i in range(0, 60)]
MINUTES_ALLOWED_MSG = "Only numbers from 0 to 59 or * are allowed."


# Hours
# =============================================================================

HOURS_RANGE = [str(i) for i in range(0, 24)]
HOURS_ALLOWED_MSG = "Only numbers from 0 to 23 or * are allowed."


# Day of month
# =============================================================================

DAY_OF_MONTH_RANGE = [str(i) for i in range(1, 32)]
DAY_OF_MONTH_ALLOWED_MSG = "Only numbers from 1 to 31 or * are allowed."
DAY_OF_MONTH_ERROR_MSG = "You set '{day_of_month}' to 'day_of_month', then 'day_of_week' must be set to '*'"


# Months
# =============================================================================

MONTHS_RANGE = ["jan", "feb", "mar", "apr", "may", "jun",
                "jul", "aug", "sep", "oct", "nov", "dec",]
MONTHS_ALLOWED_MSG = "Only numbers from 1 to 12 or * are allowed."


# Day of week
# =============================================================================

DAY_OF_WEEK_RANGE = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
DAY_OF_WEEK_ALLOWED_MSG = (
    "Only mon, tue, wed, thu, fri, sat, sun or * are allowed."
)
DAY_OF_WEEK_ERROR_MSG = "You set '{day_of_week}' to 'day_of_week', then 'months' and 'day_of_month' must be set to '*'"


# Command
# =============================================================================

COMMANDS = {
    "open": "open url",
    "cp": "copy files/folders",
    "ls": "list files",
    "cal": "cal",
}
COMMANDS_ALLOWED_MSG = f"Command allowed : {' - '.join(COMMANDS.keys())}"
