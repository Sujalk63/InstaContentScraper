def flatten_data_for_saving(data):
    """
    Flattens content-level data fetched per username for saving to Excel.
    Each post is expanded into a separate row with the username attached.
    """
    username = data.get("Username")
    content_list = data.get("content", [])

    if not content_list:
        return [{"Username": username}]

    flattened = []
    for post in content_list:
        flat_row = {"Username": username}
        flat_row.update(post)
        flattened.append(flat_row)

    return flattened
