import spawner

def make(files):
    """Given a list of files, generate a 3-dimensional list defining the
    optimal distribution of those files run across processors."""
    parallelism = spawner.parallelism()
    schedule = []

    for proc_num in range(parallelism):
        file_list = files[proc_num::parallelism]
        if len(file_list) > 0:
            schedule.append([file_list])

    return schedule

if __name__ == '__main__':
    print make_schedule(range(16))
