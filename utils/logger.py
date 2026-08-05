from datetime import datetime

LOG_FILE = "outputs/execution.log"

def write_log(option):
    with open(LOG_FILE, "a") as file:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"{current_time} : {option}\n")