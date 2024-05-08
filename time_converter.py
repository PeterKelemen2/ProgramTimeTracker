def convert_seconds(seconds):
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    to_return = f"{hours}h {minutes}m {seconds}s"
    return to_return


print(convert_seconds(10000))
