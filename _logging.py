from datetime import datetime

def log_message(path, verbose, message):
    if verbose:
        with open(path, 'a') as log_file:
            log_file.write('[{0}] {1}\n'.format(datetime.now(), message))
