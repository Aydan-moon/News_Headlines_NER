# -*- coding: utf-8 -*-
"""NLP_01.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Qt41x5PBCR_dkL2Odii173KNF9cNM7Gl

# Project 1: Named Entity Recognition (NER) for News Headlines

### **Objective**: Implement a Named Entity Recognition system to identify and classify named entities in news headlines.

**Tasks:**

Use the CoNLL-2003 dataset (English subset)

Implement data preprocessing and exploration

Train a simple NER model using spaCy's small English model

Evaluate the model's performance using precision, recall, and F1-score

Create a function to perform NER on new headlines

## Dataset Description

 **Dataset:** The CoNLL-2003 dataset is a well-known benchmark dataset in NLP, specifically designed for NER tasks. It includes annotated text data with entities categorized as:
     - `PER` (Person)
     - `ORG` (Organization)
     - `LOC` (Location)
     - `MISC` (Miscellaneous)
   - **Data Structure:**
     - The dataset is organized into sentences, where each word is tagged with its corresponding entity type or labeled as `O` if it does not belong to any named entity.
     - The dataset is split into training, validation, and test sets to facilitate model development and evaluation.

# Use the CoNLL-2003 dataset (English subset)

These libraries and functions will be used together to load a dataset, preprocess text data, train an NLP model (e.g., a named entity recognizer or text classifier), and evaluate its performance.
"""



#importing libraries
from datasets import load_dataset #Function to load datasets from Hugging Face's repository.
import spacy
from spacy.training import Example #Class for creating training examples in Spacy.
import random
from sklearn.metrics import classification_report

# Load the CoNLL-2003 dataset
dataset = load_dataset("conll2003")

train_data = dataset["train"]
test_data = dataset["test"]

"""# Implement data preprocessing and exploration

Exploring the Dataset
"""

# Display the structure of the dataset
print(dataset)

# Display a sample from the training data
print(train_data[0])
print(train_data[2])

"""### Implement data preprocessing





"""

"""
      The code is designed to map the integer NER tags found in the dataset to their corresponding string labels,
      such as "B-PER" for the beginning of a person entity.

"""
ner_labels = dataset["train"].features["ner_tags"].feature
id2label = ner_labels.int2str


"""
     Convert the data into a format suitable for model training, typically a list of sentences
      where each sentence is a list of tuples containing (word, POS, chunk, NER).

"""
# Preprocess the data
#creating a function to store data in a list
def preprocess_data(data):
    processed_data = []
    #looping through data
    for sentence in data:
        processed_sentence = []
        #looping through procesed_sentence
        for word, postag, chunk, ner in zip(sentence["tokens"], sentence["pos_tags"], sentence["chunk_tags"], sentence["ner_tags"]):
            processed_sentence.append((word, postag, chunk, id2label(ner)))
            #appending sentences to processed_data list
        processed_data.append(processed_sentence)
    return processed_data

train_data = preprocess_data(train_data)
test_data = preprocess_data(test_data)
# printing stored data
print(train_data)
print(test_data)

"""### Prepare Data for spaCy




"""

"""
    This function prepare training dataset in spaCy's format
    Training dataset has to be stored as a dictionary for further modeling NER.


"""

def convert_to_spacy_format(data):
    spacy_data = []
    for example in data:
        words = [token for token, postag, chunk, label in example]
        entities = []
        start = 0
       #This loop iterates over the words and their corresponding NER labels.
        for word, label in zip(words, [label for token, postag, chunk, label in example]):
            if label != 'O':
                entity = (start, start + len(word), label)
                entities.append(entity)
            start += len(word) + 1
        spacy_data.append((' '.join(words), {"entities": entities}))
    return spacy_data

train_data_spacy = convert_to_spacy_format(train_data)
test_data_spacy = convert_to_spacy_format(test_data)

# Display a sample from the training data
print(train_data_spacy[0])
print(train_data_spacy[3])

"""# Training a simple NER model using spaCy's small English model

* The code loads a small English model from SpaCy and disables all pipeline components except for NER.
* It creates an optimizer and then trains the NER model for 3 iterations using shuffled training data.
* The training process includes updating the model based on examples and printing out the loss after each iteration to track the model's performance.
"""

# Load the small English model
nlp = spacy.load("en_core_web_sm")

# Disable other pipelines
other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
nlp.disable_pipes(*other_pipes)

# Creating an optimizer that will be used to update the model's weights during training
optimizer = nlp.create_optimizer()

# Training the model
for i in range(3):  # Number of iterations (epochs)
    # Shuffle the training data to prevent the model from learning order-specific patterns
    random.shuffle(train_data_spacy)
    losses = {}
    for texts, annotations in train_data_spacy:
        doc = nlp.make_doc(texts)
        example = Example.from_dict(doc, annotations)  # Create an Example object that pairs the Doc with its annotations (e.g., entities)
        nlp.update([example], drop=0.5, sgd=optimizer, losses=losses)
    print(f"Iteration {i} - Losses: {losses}")

"""### Saving Model"""

# After training the model
output_dir = r"C:\Users\Lenovo\Desktop\my_projects\trained_spacy_model"  # Define the path to save the model

# Save the model to the specified directory
nlp.to_disk(output_dir)

# Output the path to the saved model
print(f"Model saved to {output_dir}")

"""# Evaluate the Model

"""

"""
      The function evaluate_model is designed to evaluate a SpaCy NLP model using metrics like Precision, Recall, and F1-score.
      It takes an NLP model (nlp) and a test dataset (data) as inputs.

"""

def evaluate_model(nlp, data):
    true_labels = []
    pred_labels = []

    for example in data:
        words = [token for token, postag, chunk, label in example]
        true_labels.extend([label for token, postag, chunk, label in example])

        # Process the text with the NLP model
        doc = nlp(' '.join(words))

        pred_index = 0

        for token in doc:
            if token.ent_iob_ == 'O':
                pred_labels.append('O')
            else:
                pred_labels.append(token.ent_type_)
            pred_index += 1

       # Check for discrepancies between the length of predicted and true labels
        # If there are fewer predicted labels, append 'O' until the lists are of equal length
        while len(pred_labels) < len(true_labels):
            pred_labels.append('O')

      # If there are more predicted labels, remove the excess labels until the lists are of equal length
        while len(pred_labels) > len(true_labels):
            pred_labels.pop()
    print(classification_report(true_labels, pred_labels))

# Evaluate on the test data
evaluate_model(nlp, test_data)

"""### *Summary of Evaluation*

The model performs well overall with 91% accuracy.

It performs best in the most general class (O) specific to NER tasks.

Improvements can be made to detect less frequent and more complex objects, such as B-PER and I-MISC.

# Create a function to perform NER on new headlines
"""

# Creating a function to perform NER on new headlines
def perform_ner(text, nlp):
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

# Example usage:
# Load the trained SpaCy model
nlp = spacy.load(r"C:\Users\Lenovo\Desktop\my_projects\trained_spacy_model")  # trained model path

# Test the function
new_headline = "The European Commission said on Thursday it disagreed with German advice to consumers to shun British lamb until scientists determine whether mad cow disease can be transmitted to sheep ."
entities = perform_ner(new_headline, nlp)
print(entities)