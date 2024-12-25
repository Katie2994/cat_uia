import cv2
import numpy as np
import random

class VideoToAscii:
    def __init__(self, video_path, width=90, height=45):  # Adjusted default size
        self.video_path = video_path
        self.width = int(width * 0.6)  # Reduce width to better match aspect ratio
        self.height = int(height * 0.6)
        self.video_capture = cv2.VideoCapture(video_path)

        # Simplified character set for the cat
        self.cat_chars = "CAT"  # Focus on CAT characters
        self.bg_chars = " "     # Blank background

    def _pixel_to_ascii(self, pixel, is_cat):
        """
        Map pixel brightness to an ASCII character.
        """
        brightness = pixel / 255  # Normalize brightness to 0-1
        char_set = self.cat_chars if is_cat else self.bg_chars
        index = int(brightness * (len(char_set) - 1))
        return char_set[index]

    def _apply_color(self, char, is_cat):
        """Apply colors to characters."""
        reset = "\033[0m"
        if is_cat:
            colors = [
                "\033[91m",  # Red
                "\033[92m",  # Green
                "\033[94m",  # Blue
                "\033[93m",  # Yellow
                "\033[95m",  # Magenta
                "\033[96m",  # Cyan
            ]
            color = random.choice(colors)
            return f"{color}{char}{reset}"
        else:
            return f"\033[97m{char}{reset}"  # White for background

    def _enhance_edges(self, frame):
        """Use edge detection to refine the cat's shape."""
        grayscale_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(grayscale_frame, 50, 150)  # Edge detection
        return edges

    def _frame_to_ascii(self, frame):
        """Convert a video frame to ASCII art."""
        resized_frame = cv2.resize(frame, (self.width, self.height))
        grayscale_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)
        edges = self._enhance_edges(resized_frame)

        # Combine edges and brightness for refined masking
        combined_mask = cv2.addWeighted(edges, 1, grayscale_frame, 0.5, 0)
        _, mask = cv2.threshold(combined_mask, 128, 255, cv2.THRESH_BINARY_INV)

        ascii_frame = []
        for y in range(self.height):
            line = ""
            for x in range(self.width):
                is_cat = mask[y, x] > 0
                char = self._pixel_to_ascii(grayscale_frame[y, x], is_cat)
                colored_char = self._apply_color(char, is_cat)
                line += colored_char
            ascii_frame.append(line)

        return ascii_frame

    def display_video_ascii(self):
        """Display video as ASCII art."""
        while True:
            ret, frame = self.video_capture.read()
            if not ret:
                break

            ascii_frame = self._frame_to_ascii(frame)
            print("\033c", end="")  # Clear the console
            for line in ascii_frame:
                print(line)
            cv2.waitKey(30)  # Adjust playback speed

        self.video_capture.release()

if __name__ == "__main__":
    video_path = "cat.mp4"  # Replace with your video's file path
    video_to_ascii = VideoToAscii(video_path, width=100, height=50)
    video_to_ascii.display_video_ascii()
