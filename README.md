# Scrapbook Wallpaper

This is a script that takes a folder of images and a base image, and turns it into a scrapbook wallpaper. It's a fun way to display your favorite images on your desktop.

![Example Scrapbook](_images/scrapbook.jpg)

_The script ensures your most recent screenshot is at the front!_

## How to use

1. Clone the repository
2. Make a folder that will hold all of your scrapbook images
3. Replace `base_image_path`, `input_folder`, and `output_image_path` with the appropriate paths
4. `python scrapbook.py`
5. Check out your scrapbook at `output_image_path`!

## Automation with your desktop wallpaper

### Mac

I have my screenshot tool (`cmd` + `shift` + `5`) set to save to the `input_folder` by default. Quick tip: if you use the `cmd` + `shift` + `4` tool, you can hold `control` to copy the screenshot to your clipboard instead of saving it to the folder for other uses.

I also use MacOS automator to watch over my scrapbook folder and run my script whenever a new image is added. Here's how to do that:

![Automator Workflow](_images/automator-script.png)

Lastly, I have my desktop wallpaper set to cycle through the `output_image_path` every 5 seconds. This way, my wallpaper is always up to date with my latest screenshots.

### Windows and Linux

TBD

## Updates

Just hit me up on any platform and I'll be happy to make this work for you! I'm also open to pull requests.
