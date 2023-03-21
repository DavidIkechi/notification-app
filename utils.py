# for adding utlity functions
def get_offset(page: int, page_size: int) -> int:
    return (page - 1) * page_size