from typing import Any, List, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
import multiprocessing


def concurrently_process(
    func: Any, tasks: List[Any], max_threads: int = multiprocessing.cpu_count()
) -> List[Tuple[Any, Optional[Exception]]]:
    """
    Runs a function in multiple threads.
    This function executes the passed in function on items in the list of tasks concurrently. If there
    is an exception when processing the tasks the list of returned tasks will include the exception
    which should be handled by the client.
    Args:
        func: A function that takes in a single input.
        tasks: Collection of inputs to the func.
        max_threads: number of threads in the thread pool defaults to 10.
    Returns:
        A list of tuples the return values from the passed in function.
    """

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        results: List[Tuple[Any, Optional[Exception]]] = []
        future_to_data = {executor.submit(func, task): task for task in tasks}
        for future in as_completed(future_to_data):
            try:
                results.append((future.result(), None))
            except Exception as exc:
                results.append((None, exc))
        return results
