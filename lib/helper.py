import time

from selenium.common.exceptions import NoSuchElementException


def timeout(true_false_method, ongoing_msg="Still not found what we were looking for", timeout_msg="Timed out!", timeout_value=None, add=0, tick=0.2):
    """
    Generic method to wait for something
    @param true_false_method: method that returns True (or an object) when wait is over, False or None otherwise
    @param ongoing_msg: message to display while waiting for timeout
    @param timeout_msg: the timeout error message
    @param timeout_value: the timeout in seconds
    @param add: add some explicit wait time
    @param tick: time between checks
    @return: None if name found. Raise an exception if not
    """
    if timeout_value is None:
        timeout_value = 10

    start_time = int(time.time())
    end_time = start_time + timeout_value
    previous_tick = time.time()
    while int(time.time()) - start_time < timeout_value:

        result = true_false_method()
        if result:
            if add > 0:
                print(add, "Additional wait time asked by user")
                time.sleep(add)
            return result

        # Print correct message
        timeout_print = int((end_time - time.time()) * 100) / 100
        if timeout_print < 0:
            print(f"{ongoing_msg}...TIMED OUT")
        else:
            print(f"{ongoing_msg}...{timeout_print}s until timeout")

        wait_time = int((tick - (time.time() - previous_tick)) * 100) / 100
        if wait_time > 0:
            time.sleep(wait_time)

        # Update previous_tick
        previous_tick = time.time()

    raise TimeoutError(timeout_msg)


def wait_exists(exists_callback, ongoing_msg=None, timeout_msg=None, timeout_value=10, add=0, tick=0.2):
    def true_false_method():
        try:
            exists_callback()
        except NoSuchElementException:
            return False
        else:
            return True

    if not ongoing_msg:
        ongoing_msg = f"Still not found what {exists_callback.__name__} is supposed to return"

    if not timeout_msg:
        timeout_msg = f"Didn't find what {exists_callback.__name__} is supposed to return !"

    timeout(true_false_method, ongoing_msg=ongoing_msg, timeout_msg=timeout_msg,
            timeout_value=timeout_value, add=add, tick=tick)
