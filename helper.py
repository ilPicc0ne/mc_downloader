
suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']

def humansize(nbytes):
    i = 0
    while nbytes >= 1024 and i < len(suffixes)-1:
        nbytes /= 1024.
        i += 1
    f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
    return '%s %s' % (f, suffixes[i])

def print_status(items_in_qeue, size_remaining, size_downloaded, description):
    print(f'Qeue Items: {items_in_qeue}, Remaining: {humansize(size_remaining)}, Downloaded: {humansize(size_downloaded)}, {description}')