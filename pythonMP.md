# 线程池和直接start区别
GitHub Copilot: `apply_async` and `start` are both methods used to start a new process in Python's `multiprocessing` module, but they have some differences.

`start` is a method of the `Process` class that starts a new process and runs the target function in that process. It returns immediately and does not wait for the process to finish. 

`apply_async` is a method of the `Pool` class that schedules a function to be executed asynchronously. It returns an `AsyncResult` object immediately, which can be used to check the status of the function and get its result when it is finished. 

The main difference between the two is that `start` creates a new process for each target function, while `apply_async` schedules the function to be executed in an existing process in a pool of processes. This means that `apply_async` can be more efficient when you need to execute many small tasks, as it avoids the overhead of creating and destroying processes for each task.

In the code you provided, `Process` and `start` are used to create two new processes and run the `process_A` and `process_B` functions in parallel. If you were to use `apply_async` instead, you would need to create a `Pool` object and use its `apply_async` method to schedule the functions to be executed in the pool.