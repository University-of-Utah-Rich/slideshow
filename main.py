import pygame
import os
import sys
import camera
import readline
import logging


class Timer:
    def __init__(self) -> None:
        self.start_time = 0

    def reset(self):
        '''
        Set the start time to the current time
        '''
        self.start_time = pygame.time.get_ticks()

    def elapsed(self):
        return pygame.time.get_ticks() - self.start_time


def load_images_from_folder(folder, start, end) -> tuple:
    '''Load a given number of images from a folder into a list of Pygame images

    Load images beginning at the start index and ending at the end index (exclusive) from the given folder into a list of Pygame images.

    Parameters
    ----------
    folder : str The folder containing the images
    start : int The index of the first image to load
    end : int The index of the last image to load (exclusive)

    Returns
    -------
    tuple(list, bool, int) A tuple containing a list of Pygame images, a boolean indicating whether the last image was loaded, and the index of the last image loaded
    '''
    last_img = False
    image_files = [os.path.join(folder, f) for f in os.listdir(
        folder) if f.endswith(".jpg") or f.endswith(".png")]
    if len(image_files) == 0:
        raise Exception("No images found in the given folder")
    if len(image_files) < end:
        end = len(image_files)
        last_img = True
    return ([pygame.image.load(f).convert() for f in image_files[start:end]], last_img, end)


def capture_img(cam, img_path, imgs_displayed):
    img = camera.get_image(cam)
    logging.info("Capturing image...")
    if img is not None:
        img.save(os.path.join(img_path, str(imgs_displayed) + ".jpg"))
        return True
    return False


def draw_frame(surface, screen, display_info):

    # Clear the screen
    screen.fill((0, 0, 0))

    # Calculate the center of the screen
    center_x = display_info.current_w / 2
    center_y = display_info.current_h / 2

    img_width, img_height = surface.get_size()

    # Calculate the position to center the image on the screen
    img_x = center_x - img_width / 2
    img_y = center_y - img_height / 2

    # Draw the current image to the screen
    screen.blit(surface, (img_x, img_y))
    pygame.display.flip()


def should_load_new_images(imgs_displayed, num_images, last_img):
    # Load new images if the last image was displayed and there are more images to load
    return imgs_displayed >= num_images - 1 and not last_img


def main():
    # check for help flag
    port = None
    if len(sys.argv) > 1 and sys.argv[1] == "-h":
        print("Usage: python3 main.py [image_folder] [delay] [img_path]")
        print("")
        print("Arguments:")
        print("image_folder: The path to the folder containing the images")
        print("delay: The delay between each image (in milliseconds)")
        print("img_path: The path to the folder where the images will be saved")
        print("port: The port number of the camera")
    # Prompt user for inputs unless they are provided as command line arguments
    if len(sys.argv) > 1:
        image_folder = sys.argv[1]
        delay = int(sys.argv[2])
        img_path = sys.argv[3]
        if len(sys.argv) > 4:
            port = sys.argv[4]

    else:
        image_folder = os.path.realpath(os.path.expanduser(
            input("Enter the path to the folder containing the images: ")))
        delay = int(
            input("Enter the delay between each image (in milliseconds): "))
        img_path = input(
            "Enter the path to the folder where the images will be saved: ")

    # save prompt inputs to history file
    # so that they can be accessed using the up arrow
    readline.write_history_file('.python_history')

    # Connect to the camera
    cam = camera.connect(port)

    # Set up the Pygame environment
    pygame.init()
    screen = pygame.display.set_mode((0, 0))
    clock = pygame.time.Clock()

    # Set the initial image and start time
    img_idx = 0

    # Main loop
    start_index = 0
    end_index = 100
    imgs_displayed = 0
    last_img = False
    images = []
    img_captured = False
    timer = Timer()
    timer.reset()
    load_new_images = True
    fullscreen = True
    while True:
        # Check for pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                screen = pygame.display.set_mode((800, 600))
                fullscreen = False
                draw_frame(images[img_idx], screen, pygame.display.Info())
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_f and not fullscreen:
                screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                fullscreen = True
                draw_frame(images[img_idx], screen, pygame.display.Info())

        # Handle the loading of images in batches of 100
        # As well as the loading of the last batch of images
        # And the stopping of the program when the last image is displayed
        if load_new_images:
            if (last_img):
                break
            # Load the next 100 images and set the start index to the last image.
            # This is done to prevent loading the same images multiple times.
            # If the last image was loaded, set the end index to the last image
            # This is done to prevent attempting to load images that don't exist
            images, last_img, start_index = load_images_from_folder(
                image_folder, start_index, end_index)
            load_new_images = should_load_new_images(
                imgs_displayed, len(images), last_img)
            # If the last image was loaded, set the end index to the last image
            if not last_img:
                end_index = start_index + 100
            else:
                end_index = start_index

        elapsed_time = timer.elapsed()

        # Handle the display of the next image
        # And the resetting of the start time and captured image flag
        if elapsed_time >= delay or imgs_displayed == 0:
            img_idx = (img_idx + 1) % len(images)
            img = images[img_idx]
            timer.reset()
            imgs_displayed += 1
            img_captured = False
            draw_frame(img, screen, pygame.display.Info())
            timer.reset()

        # Handle the capture of the image
        # This is done after the delay/2 to ensure that the correct image is being displayed
        elif elapsed_time >= delay/2 and not img_captured:
            img_captured = capture_img(cam, img_path, imgs_displayed)

        # Wait for the next frame
        clock.tick(60)


def setup():
    '''
    Set up the Python environment for the program
    '''

    readline.set_completer_delims(' \t\n=')
    readline.parse_and_bind("tab: complete")
    if os.path.exists('.python_history'):
        if os.path.getsize('.python_history') > 100:
            readline.clear_history()  # clear history if it's too large
        readline.read_history_file('.python_history')
    else:
        # create the file if it doesn't exist
        open('.python_history', 'w').close()
    if os.environ.get('DEBUG') == '1':
        logging.basicConfig(level=logging.DEBUG)


if __name__ == "__main__":
    setup()
    main()
