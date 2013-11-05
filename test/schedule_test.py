from parallelizer import scheduler

def basic_test():
    """Ensure the scheduler finds the optimal solution for a trivial input"""
    report = [
      { 'file_name': 'a', 'timing': 1 },
      { 'file_name': 'b', 'timing': 2 },
      { 'file_name': 'c', 'timing': 3 },
      { 'file_name': 'd', 'timing': 3 },
      { 'file_name': 'e', 'timing': 4 },
      { 'file_name': 'f', 'timing': 5 },
      { 'file_name': 'g', 'timing': 6 }
    ]
    schedule = scheduler.make(report, 4)
    schedule = [ set(s) for s in schedule ]

    assert(len(schedule) == 4)
    assert(set(['a', 'f']) in schedule)
    assert(set(['b', 'e']) in schedule)
    assert(set(['c', 'd']) in schedule)
    assert(set(['g']) in schedule)

def extra_cpu_test():
    """Ensure the schedule does not generate empty lists for unused
    processors"""
    report = [
      { 'file_name': 'a', 'timing': 1 }
    ]
    schedule = scheduler.make(report, 8)

    assert(len(schedule) == 1)
    assert(schedule[0] == ['a'])
