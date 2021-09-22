# overlay_victor_video
extract and overlay text to zip files videos created by Victor for use with Victor Player

The Victor Player software errors out on Windows 10 with ADSDK errors. It could be playing the videos contained in the zip files and then, BAM, you get the ADSDK error. They don't offer support unless you are certified. While you can start a Windows Sandbox and run the Victor Player, it is slow.

The purpose of this script is to read the manifest.xml file in the zip, extract the video (with path), and overlay the video with a location and timestamp at the bottom of the screen.
