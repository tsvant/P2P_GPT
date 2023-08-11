import os

def load_checkpoint(output_folder):
    """Load the last processed file index from the checkpoint file."""
    checkpoint_file = os.path.join(output_folder, 'checkpoint.txt')

    if os.path.isfile(checkpoint_file):
        with open(checkpoint_file, 'r', encoding='utf-8') as file:
            return int(file.read().strip())

    return 0
