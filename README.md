

# Data Driven Interactive Story Generation

How it works?

This is an interactive story generating system that uses human authoring along with the system's expertise to generate intriguing short stories. The system generates the first sentence of the story following which it makes suggestions for the next sentence. You can choose from the suggestions you see in the list or you can eneter a sentence which then becomes the part of the narration. This procedure continues till we have a short 5 sentence story.

* interface.ipynb runs the main code in python notebook environment (colab or jupyter)
* Requires skip-thought model that can be installed following instructions here: https://github.com/ryankiros/skip-thoughts
* Requires trained models which are about 4 GB in size and available here: https://drive.google.com/drive/folders/1f-MtdTKIcm9psEKYxn9hVw5Y6UfnG9eg?usp=sharing
* Requires pytorch, numpy, seaborn, pandas, theano
* Requires train_vectors.npy and train_sentences.npy available here: https://drive.google.com/open?id=1jOFv0ZokHCA2tLPzD6yITl0Stf0MjhDR

* seperate_model.ipynb notebook trains the models.
* Results.ipynb tests the models and generates results.
* data_preprocessing.py processes the raw data (requires Stanford Core NLP).
