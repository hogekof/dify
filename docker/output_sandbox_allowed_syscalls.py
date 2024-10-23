import os
from dotenv import load_dotenv

load_dotenv()

default_allowed_syscalls = [int(x) for x in os.environ['DEFAULT_ALLOWED_SYSCALLS'].split(',')]
add_allowed_syscalls = [int(x) for x in os.environ['ADD_ALLOWED_SYSCALLS'].split(',')]

add_allowed_syscalls = sorted(list(set(add_allowed_syscalls) | set(default_allowed_syscalls)))
print(','.join([str(x) for x in add_allowed_syscalls]))
