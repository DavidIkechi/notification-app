from enum import Enum
# for adding utlity functions
def get_offset(page: int, page_size: int) -> int:
    return (page - 1) * page_size

# define the enum type for the status.
class Status(Enum):
    IN_PROGRESS = 'processing'
    SUCCESS = 'success'
    QUEUED = 'queue'
    FAILED = 'failed'