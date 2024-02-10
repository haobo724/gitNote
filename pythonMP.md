# python多线程/进程自我学习笔记


## 进程池和直接start区别
GitHub Copilot: `apply_async` and `start` are both methods used to start a new process in Python's `multiprocessing` module, but they have some differences.

`start` is a method of the `Process` class that starts a new process and runs the target function in that process. It returns immediately and does not wait for the process to finish. 

`apply_async` is a method of the `Pool` class that schedules a function to be executed asynchronously. It returns an `AsyncResult` object immediately, which can be used to check the status of the function and get its result when it is finished. 

The main difference between the two is that `start` creates a new process for each target function, while `apply_async` schedules the function to be executed in an existing process in a pool of processes. This means that `apply_async` can be more efficient when you need to execute many small tasks, as it avoids the overhead of creating and destroying processes for each task.

In the code you provided, `Process` and `start` are used to create two new processes and run the `process_A` and `process_B` functions in parallel. If you were to use `apply_async` instead, you would need to create a `Pool` object and use its `apply_async` method to schedule the functions to be executed in the pool.

## 进程池使用时可能和queue会有冲突
进程池（Pool）和队列（Queue）在一些实现上有一些微妙的交互，可能导致死锁。具体来说，Pool 用它自己的Queue来管理工作进程之间的通讯，当你尝试在一个进程池的工作进程中使用另一个Queue（或者其他 IPC 对象，如锁）时，可能会导致死锁。Pool.apply_async() 方法在调用目标函数之前获取一个全局的进程池锁，而这个锁可能与你自己创建的队列交互，从而导致进程无响应。

解决办法：使用Manager.Queue