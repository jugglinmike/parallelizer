from parallelizer import scheduler

def basic_test():
    """Ensure the scheduler finds the optimal solution for a trivial input"""
    report = [
      { 'file_name': 'a', 'weight': 1 },
      { 'file_name': 'b', 'weight': 2 },
      { 'file_name': 'c', 'weight': 3 },
      { 'file_name': 'd', 'weight': 3 },
      { 'file_name': 'e', 'weight': 4 },
      { 'file_name': 'f', 'weight': 5 },
      { 'file_name': 'g', 'weight': 6 }
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
      { 'file_name': 'a', 'weight': 1 }
    ]
    schedule = scheduler.make(report, 8)

    assert(len(schedule) == 1)
    assert(schedule[0] == ['a'])
