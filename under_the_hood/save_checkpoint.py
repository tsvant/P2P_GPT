import os

def save_checkpoint(output_folder, file_index):
    """Save the current file index to a checkpoint file."""
    checkpoint_file = os.path.join(output_folder, 'checkpoint.txt')

    with open(checkpoint_file, 'w', encoding='utf-8') as file:
        file.write(str(file_index))
