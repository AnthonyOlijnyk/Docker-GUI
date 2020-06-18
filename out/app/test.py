import os
import numpy as np
import SimpleITK as sitk
from pathlib import Path
from skimage.transform import resize
import matplotlib.pyplot as plt

import tensorflow as tf
from tensorflow.keras.models import load_model

def predictVol(vol, model, model_inputdim):
    og_dim = vol.shape
    
    vol = resize(vol, (vol.shape[0], model_inputdim[0], model_inputdim[1]))
    vol = (vol/np.max(vol)) * 255
        
    j = 0
    
    im = vol[j,:,:] 
    im = np.expand_dims(im, axis=-1)
    im = np.concatenate((im, im, im), axis=-1)
    
    im = np.expand_dims(im, axis=0)
    im = tf.keras.applications.vgg19.preprocess_input(im)
    
    print("three")
    im_pred = model.predict(im)
    
    vol_out = im_pred[0,:,:,0]
    vol_out = binarize(vol_out)
    vol_out = np.expand_dims(vol_out, axis = 0)
    
    for j in range(1,vol.shape[0]):
        im = vol[j,:,:] 
        im = np.expand_dims(im, axis=-1)
        im = np.concatenate((im, im, im), axis=-1)
        
        im = np.expand_dims(im, axis=0)
        im = tf.keras.applications.vgg19.preprocess_input(im)
        
        im_pred = model.predict(im)
        
        vol_pred = im_pred[0,:,:,0]
        vol_pred = binarize(vol_pred)
        vol_pred = np.expand_dims(vol_pred, axis = 0)
        
        vol_out = np.concatenate((vol_out, vol_pred), axis=0)
        
    vol_out = resize(vol_out, (vol.shape[0], og_dim[1], og_dim[2]))
    if np.max(vol_out)>0:
        vol_out = vol_out/np.max(vol_out)
    
    vol_out = binarize(vol_out)
    
    return vol_out 

def binarize(arr):
    arr_b = arr
    arr_b[arr_b >= 0.5] = 1
    arr_b[arr_b < 0.5] = 0
    return arr_b

#%% Setup
print("one")
model_inputdim = [224, 224]
input_folder = Path(os.path.join(os.getcwd(), 'data'))
input_list = os.listdir(input_folder)

model_folder = Path(os.path.join(os.getcwd(), 'model') )
model_list = os.listdir(model_folder)

model = load_model(model_folder/model_list[0], compile = False) # Assuming only one model

pred_folder = Path(os.path.join(os.getcwd(), 'prediction'))
if not os.path.exists(pred_folder):
    os.makedirs(pred_folder)

#%% Prediction

print("two")
for file in input_list:
    input_name = os.path.join(input_folder, file)
    input_vol = np.array(sitk.GetArrayFromImage(sitk.ReadImage(input_name)))

    pred_vol = predictVol(input_vol, model, model_inputdim)
    
    sitk.WriteImage(sitk.GetImageFromArray(pred_vol), os.path.join(pred_folder, file))

#%% Sample
print("four")
fig, (ax1, ax2) = plt.subplots(1, 2)
fig.suptitle('Sample of Predictions')
ax1.imshow(input_vol[24,:,:])
ax2.imshow(pred_vol[24,:,:])
print(input_vol)
print(pred_vol)

plt.savefig(pred_folder/'sample.png', dpi = 400)






