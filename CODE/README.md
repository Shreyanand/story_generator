* interface.ipynb is the main file for running the code
* It can be run in any python notebook environment (colab or jupyter)
* It requires skip-thought model that can be installed following instructions here: https://github.com/ryankiros/skip-thoughts
* It requires trained models which are about 4 GB in size and available here: https://drive.google.com/drive/folders/1f-MtdTKIcm9psEKYxn9hVw5Y6UfnG9eg?usp=sharing
* It requires pytorch, numpy, seaborn, pandas, theano 
* It requires train_vectors.npy and train_sentences.npy available here: https://drive.google.com/open?id=1jOFv0ZokHCA2tLPzD6yITl0Stf0MjhDR


* The entire code is on the github: https://github.ncsu.edu/sanand3/story_cloze/tree/New_arch

* seperate_model.ipynb was used for training the model.
* Results.ipynb was used for testing and generating results.
* data_preprocessing.py was used for data preprocessing (requires Stanford Core NLP).

* seperate_models folder contains preprocessed data, and skip thought vectors
of the train and test set.
