def size2str(size: int) -> str:
    def round2str(a, b) -> str:
        return str(round(a, b))

    STEP = 1024
    KB = STEP
    MB = KB * STEP
    GB = MB * STEP

    if size >= GB:
        return round2str(size / GB, 2) + " GB"
    elif size >= MB:
        return round2str(size / MB, 2) + " MB"
    elif size >= KB:
        return round2str(size / KB, 2) + " KB"
    else:
        return str(size)
