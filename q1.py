from random import randint, sample
class Process:
    def __init__(self, accessed_pages: list, duration: int) -> None:
        self.accessed_pages = accessed_pages
        self.duration = duration

PAGE_QUANTITY = 15
PROCESS_QUANTITY = 50
PROCESS_MAX_DURATION = 100
PROCESS_MIN_DURATION = 1

def create_processes(page_quantity=PAGE_QUANTITY, process_quantity=PROCESS_QUANTITY):
    processes = []
    for _ in range(process_quantity):
        accessed_pages = sample(list(range(1, page_quantity)), randint(1, page_quantity))
        new_process = Process(accessed_pages, duration=randint(PROCESS_MIN_DURATION, PROCESS_MAX_DURATION))
        processes.append(new_process)
    return processes

def FIFO(frame_quantity):
    memory = []
    count_page_fault = 0
    processes = create_processes()
    for process in processes:
        for page in process.accessed_pages:
            if page not in memory:
                count_page_fault+=1
                if len(memory) >= frame_quantity:
                    memory.pop(0)
                memory.append(page)
    
def Aging(frame_quantity):
    pass
