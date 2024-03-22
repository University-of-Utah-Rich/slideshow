Here's a README.md for your code:

```markdown
# Pygame Image Viewer and Camera Capture

This Python program is a simple image viewer and camera capture tool using Pygame and a custom camera module. It displays images from a specified folder one by one at a specified delay and captures images from a connected camera.

## Features

- Display images in full-screen mode or in a windowed mode.
- Switch between full-screen and windowed mode using keyboard shortcuts.
- Load and display images from a specified directory.
- Capture images from the camera and save them to a specified directory.
- Handles user input for exiting the program and toggling screen modes.

## Requirements

- Python 3
- Pygame
- OpenMV camera and libraries
- Operating system capable of running Python and Pygame

## Setup

1. Install Python 3 if you have not already done so.
2. Install Pygame using pip:

   ```bash
   pip install pygame
   ```

3. Ensure the custom camera module is correctly set up and available in your Python environment.

## Usage

1. Navigate to the directory containing the script.
2. Run the script using Python:

   ```bash
   python3 main.py [image_folder] [delay] [img_path] [port]
   ```

   - `image_folder`: The path to the folder containing the images to display.
   - `delay`: The delay between each image in milliseconds.
   - `img_path`: The path to the folder where the camera images will be saved.
   - `port`: The port number of the camera (optional).

   If you run the script without arguments, it will prompt you for these inputs.

3. Once the program is running:
   - Press `ESC` to exit.
   - Press `R` to switch to windowed mode.
   - Press `F` to switch back to full-screen mode.

## Functions

### `load_images_from_folder`

Loads a specified range of images from a folder into a list.

### `capture_img`

Captures an image from the camera and saves it to a specified path.

### `draw_frame`

Draws the current image onto the Pygame window, centering it.

### `should_load_new_images`

Determines whether new images need to be loaded based on the current index and total images.

## Customization

- Modify the image loading, display settings, or camera settings as needed.
- Adjust the screen resolution and window mode toggle functionality to suit your requirements.

## Troubleshooting

Ensure all file paths and environment settings are correctly configured. If issues persist, check the Python and Pygame documentation for additional help.

## License

Specify your license here or state if the project is open-source.

```

Note: Replace the "custom camera module (not included)" with the actual name or description of your camera handling module if it is a publicly available library, or provide the necessary details if it is a custom-built module.