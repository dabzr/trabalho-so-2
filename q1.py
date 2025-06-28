from random import choice, choices, randint, sample

class Process:
    def __init__(self, working_sets: zip) -> None:
        self.working_sets = working_sets

PAGE_QUANTITY = 15
PROCESS_QUANTITY = 50
WORKING_SET_MAX_DURATION = 50
WORKING_SET_MAX = 20
def create_processes(page_quantity=PAGE_QUANTITY, process_quantity=PROCESS_QUANTITY):
    processes = []
    for _ in range(process_quantity):
        working_set_quantity = randint(1, WORKING_SET_MAX)
        working_sets = []
        for _ in range(working_set_quantity):
            accessed_pages = sample(list(range(1, page_quantity)), randint(1, page_quantity)) # ESCOLHE N ELEMENTOS ALEATÓRIOS ÚNICOS
            working_sets.append(accessed_pages)
        durations = list(map(lambda _: randint(1, WORKING_SET_MAX_DURATION), working_sets))
        working_sets = zip(working_sets, durations)
        processes.append(Process(working_sets))
    return processes

def FIFO(frame_quantity):
    memory = []
    count_page_fault = 0
    processes = create_processes()
    for process in processes:
        for working_set, duration in process.working_sets:
            accessed_pages = choices(working_set, k=duration) # ESCOLHE K ELEMENTOS ALEATÓRIOS QUE PODEM REPETIR
            for page in accessed_pages:
                if page not in memory:
                    count_page_fault+=1
                    if len(memory) >= frame_quantity:
                        memory.pop(0)
                    memory.append(page)
   
def aging(reference_string, num_frames, bits=8):
    memory = {}
    counters = {}
    page_faults = 0

    for page in reference_string:
        for p in counters:
            counters[p] >>= 1
        if page in memory:
            counters[page] |= 1 << (bits - 1)
        else:
            page_faults += 1
            if len(memory) >= num_frames:
                to_remove = min(counters, key=lambda k: counters[k])
                del memory[to_remove]
                del counters[to_remove]
            memory[page] = True
            counters[page] = 1 << (bits - 1)

    return page_faults

