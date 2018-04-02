import numpy as np
from keras.preprocessing import image
from keras.applications import resnet50

# Load Keras' ResNet50 model that was pre-trained against the ImageNet database
model = resnet50.ResNet50()


def get_predictions(pict):
    # given an image, runs through ResNet50, and returns the top 5 results
    img = image.load_img(pict, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = resnet50.preprocess_input(x)
    predictions = model.predict(x)
    predicted_classes = resnet50.decode_predictions(predictions, top=5)
    print("This is an image of:")
    for imagenet_id, name, likelihood in predicted_classes[0]:
        print(" - {}: {:2f} likelihood".format(name, likelihood))
