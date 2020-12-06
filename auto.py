import schedule, random, time
from users import *
from main import check

minute = random.randint(1, 10)
CHECK_SCHEDULES = [
    (7, minute),
    (21, minute)
]

def check_all():
    for user in users:
        check(user['username'], user['password'])

if __name__ == "__main__":
    for i in range(len(CHECK_SCHEDULES)):
        schedule.every().day.at("{:0>2d}:{:0>2d}".format(*CHECK_SCHEDULES[i])).do(check_all)

    while True:
        schedule.run_pending()
        time.sleep(30)