import os

# Specify the directory containing the frames
directory = 'btm/test'

# Iterate over all files in the directory
for filename in os.listdir(directory):
    # Check if the file is a frame
    if filename.startswith('frame') and filename.endswith('.jpg'):
        # Extract the frame number
        frame_number = int(filename[len('frame'):-len('.jpg')])
        
        # Create the new filename
        new_filename = f'frame_{frame_number:06d}.jpg'
        
        # Get the full paths to the old and new filenames
        old_filepath = os.path.join(directory, filename)
        new_filepath = os.path.join(directory, new_filename)
        
        # Rename the file
        os.rename(old_filepath, new_filepath)

print("Renaming process is completed!")
