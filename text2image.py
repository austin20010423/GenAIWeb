# Install required packages
# pip install --quiet --upgrade --user google-cloud-aiplatform

# Initialize Vertex AI
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel
from PIL import Image
import math
import io

# Define project information
PROJECT_ID = "sunlit-inn-386509"  # @param {type:"string"}
LOCATION = "us-central1"  # @param {type:"string"}

"""
def display_images_in_grid(images):
    

    # Determine the number of rows and columns for the grid layout.
    nrows = math.ceil(len(images) / 4)  # Display at most 4 images per row
    # Adjust columns based on the number of images
    ncols = min(len(images) + 1, 4)

    # Create a figure and axes for the grid layout.
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(12, 6))

    for i, ax in enumerate(axes.flat):
        if i < len(images):
            # Display the image in the current axis.
            ax.imshow(images[i]._pil_image)

            # Adjust the axis aspect ratio to maintain image proportions.
            ax.set_aspect("equal")

            # Disable axis ticks for a cleaner appearance.
            ax.set_xticks([])
            ax.set_yticks([])
        else:
            # Hide empty subplots to avoid displaying blank axes.
            ax.axis("off")

    # Adjust the layout to minimize whitespace between subplots.
    plt.tight_layout()

    # Display the figure with the arranged images.
    plt.show()
"""


def model(text: str, negative: str = None):
    vertexai.init(project=PROJECT_ID, location=LOCATION)

    generation_model = ImageGenerationModel.from_pretrained(
        "imagegeneration@005")

    # 圖片生成指令
    prompt = text
    try:
        response = generation_model.generate_images(
            prompt=prompt,
            # 產生圖片數量
            number_of_images=1,
            # 種子亂數，保證產生相似的圖片，如果想樣要不一樣的，設 None
            seed=None,
            # 負面指令，避免不想要的元素
            negative_prompt=negative,
        )

        # 顯示圖片
        # display_images_in_grid(response.images)

        return response.images[0]._pil_image.resize((512, 512), resample=Image.LANCZOS)
    except Exception as e:
        print(e)

        return 'This Message has been blocked because it violate our Community Guidelines. Please try again'


"""

if __name__ == '__main__':

    model("a cute cartoon dog on a grass, front")
"""
