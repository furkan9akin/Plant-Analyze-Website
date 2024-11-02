from keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np

def kerass(resim):
    # Disable scientific notation for clarity
    np.set_printoptions(suppress=True)

    # Load the model
    model = load_model("plant_village_model.h5", compile=False)

    # Load the labels
    class_names = open("labels.txt", "r").readlines()

    # Create the array of the right shape to feed into the keras model
    # The 'length' or number of images you can put into the array is
    # determined by the first position in the shape tuple, in this case 1
    data = np.ndarray(shape=(1, 128, 128, 3), dtype=np.float32)

    # Replace this with the path to your image
    image = Image.open(resim).convert("RGB")

    # resizing the image to be at least 224x224 and then cropping from the center
    size = (128, 128)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

    # turn the image into a numpy array
    image_array = np.asarray(image)

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

    # Load the image into the array
    data[0] = normalized_image_array

    # Predicts the model
    prediction = model.predict(data)

    liste = []
    for i in prediction[0]:
        liste.append(round(i,10))

    


    return liste

if __name__=="__main__":
    
    x=kerass("static/img/tarim_bitki.jpg")
    print(x)