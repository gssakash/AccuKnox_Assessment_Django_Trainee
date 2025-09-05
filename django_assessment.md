## Question 1: By default are django signals executed synchronously or asynchronously? Please support your answer with a code snippet that conclusively proves your stance. The code does not need to be elegant and production ready, we just need to understand your logic.

A : The default behaviour in Django is that Signals are handled synchronously and the receivers are executed immediately whenever a signal is sent. However, they can be handled asynchronously by using tools like Celery enhancing the responsiveness of your application but understand that due to the async properties, the order of execution will not be sequential.

## Code Snippet

```python
import time
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def my_signal_receiver(sender, instance, **kwargs):
    print("Signal handler starting")
    time.sleep(5)
    print("Signal handler finished")

# Usage
user = User(username="sync_test")
user.save()
print("Completed")
```

### Expected Output
```
Signal handler starting
... (waits 5 seconds) ...
Signal handler finished
Completed
```

The Completed message appears after the handler prints "Signal handler finished", showing the save operation waits for the signal receiver to complete.
If signals were asynchronous, "Completed" message would print immediately, before the signal handler.


## Question 2: Do django signals run in the same thread as the caller? Please support your answer with a code snippet that conclusively proves your stance. The code does not need to be elegant and production ready, we just need to understand your logic.

Yes, Django signals run in the same thread as a caller without spawning another thread and signals block the current thread and run receiver functions immediately, without switching to another thread.

## Code Snippet

```python
import threading
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def my_signal_receiver(sender, instance, **kwargs):
    print("Receiver thread:", threading.current_thread().name)

user = User(username="thread_test")
print("Caller thread:", threading.current_thread().name)
user.save()
```

### Expected Output
```
Caller thread: MainThread
Receiver thread: MainThread
```

The output will show that both the caller and the receiver run in MainThread (or the same thread in multi-threaded environments).

## Question 3: By default do django signals run in the same database transaction as the caller? Please support your answer with a code snippet that conclusively proves your stance. The code does not need to be elegant and production ready, we just need to understand your logic.

By default, Django signals run in the same database transaction as the caller if a transaction is active (for example, inside an atomic block). Signals are sent immediately as part of whatever database operations triggered them, so they execute within the current transaction context.

```python
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def signal_receiver(sender, instance, **kwargs):
    print("In transaction:", transaction.get_connection().in_atomic_block)

user1 = User(username="outside_txn")
user1.save()  
print("Saved user1")

with transaction.atomic():
    user2 = User(username="inside_txn")
    user2.save()  
    print("Saved user2 inside transaction")
```

### Expected Output

```
In transaction: False
Saved user1
In transaction: True
Saved user2 inside transaction
```

When saving user1, no explicit transaction is active (autocommit mode), so the signal sees in_atomic_block = False.
When saving user2 inside the atomic block, the signal runs inside the same transaction (in_atomic_block = True).

Therefore, in signals, the current database transaction context is inherited from the caller's database operation and signals execute within the current database context that is inherited.