import os
from typing import List
from datetime import datetime
from random import choices, randint, sample

class Process:
    def __init__(self, pid: int, references: List[int]) -> None:
        self.pid = pid
        self.references = references

PAGE_QUANTITY = 15
PROCESS_QUANTITY = 50
WORKING_SET_MAX_DURATION = 50
WORKING_SET_MAX = 20

def create_processes(page_quantity=PAGE_QUANTITY, process_quantity=PROCESS_QUANTITY):
    processes = []
    for pid in range(process_quantity):
        working_set_quantity = randint(1, WORKING_SET_MAX)
        working_sets = []
        for _ in range(working_set_quantity):
            accessed_pages = sample(list(range(1, page_quantity)), randint(1, page_quantity - 1)) # ESCOLHE N ELEMENTOS ALEATÓRIOS ÚNICOS
            working_sets.append(accessed_pages)
        durations = list(map(lambda _: randint(1, WORKING_SET_MAX_DURATION), working_sets))
        references_list = (map(lambda ws: choices(ws[0], k=ws[1]), zip(working_sets, durations)))
        references = [ref for lst in references_list for ref in lst]

        processes.append(Process(pid, references))
    return processes

def FIFO(processes, frame_quantity):
    memory = []
    count_page_fault = 0

    for process in processes:
        for page in process.references:
            if page not in memory:
                count_page_fault+=1
                if len(memory) >= frame_quantity:
                    memory.pop(0)
                memory.append(page)

    return count_page_fault
   
def aging(processes, frame_quantity, decay_factor=0.5, ref_boost=1.0):
    memory = {}
    scores = {}
    page_faults = 0

    for process in processes:
        for page in process.references:
            for p in scores:
                scores[p] *= decay_factor

            if page not in memory:
                page_faults += 1
                if len(memory) >= frame_quantity:
                    to_remove = min(scores, key=lambda k: scores[k])
                    del memory[to_remove]
                    del scores[to_remove]
                memory[page] = True

            scores[page] = scores.get(page, 0) + ref_boost

    return page_faults

def total_references(processes):
    return sum(len(p.references) for p in processes)

def save_references(processes):
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")

    output_dir = "refs"
    os.makedirs(output_dir, exist_ok=True)

    base_name = f"refs_{timestamp}.txt"
    filename = os.path.join(output_dir, base_name)

    counter = 1
    while os.path.exists(filename):
        new_name = f"refs_{timestamp}_{counter}.txt"
        filename = os.path.join(output_dir, new_name)
        counter += 1

    with open(filename, "w") as f:
        for process in processes:
            f.write(f"Process #{process.pid}:\n")
            for ref in process.references:
                f.write(f"{ref}\n")
            f.write("\n")

    print(f"{filename} created.")
