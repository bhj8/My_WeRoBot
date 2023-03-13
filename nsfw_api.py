import os
import opennsfw2 as n2

def is_safe(img_path):
    nsfw_probability = n2.predict_image(img_path)
    if nsfw_probability > 0.4:
        return False
    return True


# import opennsfw2 as n2

# # To get the NSFW probability of a single image.
# image_path = "path/to/your/image.jpg"

# nsfw_probability = n2.predict_image(image_path)

# # To get the NSFW probabilities of a list of images.
# # This is better than looping with `predict_image` as the model will only be instantiated once
# # and batching is used during inference.
# image_paths = [
#   "path/to/your/image1.jpg",
#   "path/to/your/image2.jpg",
#   # ...
# ]

# nsfw_probabilities = n2.predict_images(image_paths)



# import opennsfw2 as n2

# # The video can be in any format supported by OpenCV.
# video_path = "path/to/your/video.mp4"

# # Return two lists giving the elapsed time in seconds and the NSFW probability of each frame.
# elapsed_seconds, nsfw_probabilities = n2.predict_video_frames(video_path)