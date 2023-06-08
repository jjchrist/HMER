# Handwritten math expression recognition using CNN;
#
###### Handwritten math symbols dataset from Kaggle (https://www.kaggle.com/datasets/xainano/handwrittenmathsymbols) reduced to 70 classes and approximately 500 images per class
### Language: Python (.py, .ipynb)
#### CNN built in Tensorflow
* **img_preprocess.py** - to precosess image before recognition,
* **main.py** - main file to start project with simple GUI
* **predict_fnc.py** - file with prediction functions
* **regexpr.py** - regular expression functions to prepare recognized expression before converting to LaTeX format
* **train.ipynb** - notebook with a model training, trained models are saved in 'model' directory
 
Trainig accuracy - 95%
Validation_accuracy - 94%

Model works with trigonometry, limits, algebraic equation. 
* x2 = x\*\*2 
* 3x = 3\*x
* (x+1)2 = (x+1)\*2
* 3(x+1) = 3\*(x+1)
* limits should be written like " lim(expression, variable -> value) ". They will be converted to " Limit(expression, variable, value) "

Model doesn't work with indices, definite integrals, roots.

Used libraries:
* tensorflow, keras, scikit-learn - for training and evaluating model
* opencv - for image preprocessing (resizing, denoising, thresholdinbg, segmentation)
* regex - for preparing expression to sympy format
* sympy - to parse predicted expression and covert to LaTeX
* PySimpleGUI - for simple user interface
* and others (numpy, os, etc.)
