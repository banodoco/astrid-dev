"""Record load in one process so cleanup does not orphan a sleep child."""
import datetime
import sys
import time


def main(path):
    with open(path, "a", encoding="utf-8") as output:
        while True:
            with open("/proc/loadavg", encoding="utf-8") as load:
                averages = " ".join(load.read().split()[:3])
            stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            print(stamp, averages, file=output, flush=True)
            time.sleep(30)


if __name__ == "__main__":
    main(sys.argv[1])
