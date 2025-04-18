# -*- coding: utf-8 -*-
"""IST-718_Group-2_Final_Project_Playground.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16dcoIdDuvobjrc3Jb3JaUOttRZBHytGV

# IST 718 | Final Project | Playground | Group/Team 2

### Project Overview:
- Classifying radiology images: Normal vs Pneumonia
- [Click here to find the dataset on Kaggle](https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia)

The code utilizes a pre-trained computer vision model called 'ResNet18' on radiology image data.  The model is then fine tuned on the data.  The deep learning model is tuned with three (3) epochs with a theoretical error rate of 1.1% and is exported to a `.pkl` file for future use.

### Configuring Google Drive, Kaggle
- Create free Kaggle API key
  - Needed to download the dataset from Kaggle
- Upload kaggle.json to Google Drive
  - Kaggle configuration settings
- Mount Google Drive to Colab
  - Data source copy directory
- Ensure Colab has GPU settings turned on for training
"""

!python -V

from google.colab import drive
drive.mount('/content/drive')

# Commented out IPython magic to ensure Python compatibility.
# %pwd

# Commented out IPython magic to ensure Python compatibility.
!mkdir -p
# %cd '/content/drive/MyDrive/IST 718/Final Project'

# Commented out IPython magic to ensure Python compatibility.
# %ls -a

import os
os.environ['KAGGLE_CONFIG_DIR'] = '/content/drive/MyDrive/IST 718/Final Project'

!kaggle datasets download -d paultimothymooney/chest-xray-pneumonia

!unzip '/content/drive/MyDrive/IST 718/Final Project/chest-xray-pneumonia.zip' -d '/content/drive/MyDrive/IST 718/Final Project/chest-xray-pneumonia'

"""### Review Data Samples

Examples of 3 'normal' cases:
"""

import os
import random
from PIL import Image

# Set the seed for the random number generator
random.seed(69)

# Set the path of the directory containing the images
dir_path = '/content/drive/MyDrive/IST 718/Final Project/chest-xray-pneumonia/chest_xray/train/NORMAL/'

# Get a list of all the image files in the directory
files = [f for f in os.listdir(dir_path) if f.endswith('.jpeg')]

# Choose 3 random files from the list
random_files = random.sample(files, 3)

# Loop through each file and print it to the screen as a thumbnail
for file in random_files:
    im = Image.open(os.path.join(dir_path, file))
    im.thumbnail((256, 256))
    im.show()

"""Examples of 3 'abnormal' cases:"""

# Set the seed for the random number generator
random.seed(69)

# Set the path of the directory containing the images
dir_path = '/content/drive/MyDrive/IST 718/Final Project/chest-xray-pneumonia/chest_xray/train/PNEUMONIA'

# Get a list of all the image files in the directory
files = [f for f in os.listdir(dir_path) if f.endswith('.jpeg')]

# Choose 3 random files from the list
random_files = random.sample(files, 3)

# Loop through each file and print it to the screen as a thumbnail
for file in random_files:
    im = Image.open(os.path.join(dir_path, file))
    im.thumbnail((256, 256))
    im.show()

"""### Exploring
- Ideas:
  - See how many images were in the dataset
  - See how big the files are (histogram of image sizes?)
"""



"""### Train fastai Model
- Tip
  - Make sure you have your Colab GPU settings turned on...or training will take....wait for it.....forever :-)
"""

from fastai.vision.all import *

path = Path('/content/drive/MyDrive/IST 718/Final Project/chest-xray-pneumonia/chest_xray/train')
path

dls = DataBlock(
    blocks=(ImageBlock, CategoryBlock), 
    get_items=get_image_files, 
    splitter=RandomSplitter(valid_pct=0.2, seed=1),
    get_y=parent_label,
    item_tfms=[Resize(192, method='squish')]
).dataloaders(path, bs=32)

dls.show_batch(max_n=6)

learn = vision_learner(dls, resnet18, metrics=error_rate)
learn.fine_tune(3)

import os

# Save the model for future use
learn.export(f"{os.environ['KAGGLE_CONFIG_DIR']}/IST_718_Group-2_Radiology_Model_Classifier.pkl'")

# Load the model
learn = load_learner(f"{os.environ['KAGGLE_CONFIG_DIR']}/IST_718_Group-2_Radiology_Model_Classifier.pkl'")
learn

"""### Test Prediction on Sample Image"""

is_normal,_,probs = learn.predict(PILImage.create('/content/drive/MyDrive/IST 718/Final Project/chest-xray-pneumonia/chest_xray/test/NORMAL/IM-0001-0001.jpeg'))
print(f"This is a: {is_normal}.")
print(f"Probability of normal chest x-ray without findings: {probs[0]:.4f}")

"""# Overview of Model Architecture | Diagram"""

!pip install -Uqq graphviz

import graphviz
def gv(s): 
  return graphviz.Source('digraph G{ rankdir="LR"' + s + '; }')

gv('''ordering=in
model[shape=box3d width=1 height=0.7 label=model]
inputs->model->predictions; parameters->model; labels->loss; predictions->loss
loss->parameters[constraint=false label=update]''')

"""### Predict on Test Data"""

test_path = Path('/content/drive/MyDrive/IST 718/Final Project/chest-xray-pneumonia/chest_xray/test')
test_files = get_image_files(test_path)
test_dl = dls.test_dl(test_files)
preds = learn.get_preds(dl=test_dl)

pred_labels = preds[0].argmax(dim=1)
pred_labels

pred_class_names = [dls.vocab[label] for label in pred_labels]
pred_class_names

true_labels = [parent_label(img) for img in test_files]
correct_predictions = sum([true == pred for true, pred in zip(true_labels, pred_class_names)])
accuracy = correct_predictions / len(test_files) * 100

for img_file, pred_class in zip(test_files, pred_class_names):
    print(f"{img_file}: {pred_class}")

print(f"Accuracy: {accuracy:.2f}%")