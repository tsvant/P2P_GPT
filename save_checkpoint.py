import os
import threading

# Create a global lock
checkpoint_lock = threading.Lock()


def save_checkpoint(output_folder, file_index):
    """Save the current file index to a checkpoint file."""
    checkpoint_file = os.path.join(output_folder, 'checkpoint.txt')

    # Only one thread can hold the lock at a time
    with checkpoint_lock:
        with open(checkpoint_file, 'w', encoding='utf-8') as file:
            file.write(str(file_index))