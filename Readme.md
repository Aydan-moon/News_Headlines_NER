# Named Entity Recognition (NER) for News Headlines

### Project Overview
This project implements a Named Entity Recognition (NER) system designed to identify and classify named entities (e.g., persons, organizations, locations) in news headlines. The system is built using **spaCy** and trained on the **CoNLL-2003 dataset**. 

### Project Objectives
- Use the CoNLL-2003 dataset to build and train an NER model.
- Implement data preprocessing and exploratory analysis.
- Train a simple NER model using spaCy's small English model.
- Evaluate the model using precision, recall, and F1-score metrics.
- Create a function to perform NER on new, unseen headlines.

---

## Dataset Description
**Dataset**: [CoNLL-2003](https://huggingface.co/datasets/conll2003), a well-known benchmark for NER tasks, containing:
- `PER` (Person)
- `ORG` (Organization)
- `LOC` (Location)
- `MISC` (Miscellaneous)

**Structure**: Each word in a sentence is tagged with an entity type or labeled as `O` if it doesn't belong to any named entity. The dataset is split into training, validation, and test sets to ensure fair model evaluation.

---

## Project Workflow

### 1. Data Preprocessing
- **Data Loading**: The dataset is loaded using the Hugging Face `datasets` library.
- **Data Exploration**: Initial exploration provides insights into the distribution of entity labels and helps prepare data for modeling.
- **Data Preparation**: The data is converted into a format compatible with spaCy for training.

### 2. Model Training
- **Model Selection**: We use spaCy’s small English model, focusing solely on the NER component.
- **Training Process**: The NER model is trained over multiple iterations, adjusting parameters to improve performance.
- **Model Saving**: The trained model is saved for later use and evaluation.

### 3. Model Evaluation
- **Metrics**: The model’s performance is evaluated using:
  - **Precision**
  - **Recall**
  - **F1-score**

The model achieves high accuracy, especially in identifying common entity types. Performance insights suggest potential for improvement in detecting less frequent entity types.

### 4. Performing NER on New Headlines
A function is created to perform NER on new text data. Given a headline, the function identifies and classifies entities, providing quick insights into the headline's key terms.

---

## Usage

### Prerequisites
- Python 3.7+
- Install required libraries:
  ```bash
  pip install spacy datasets


### Running the Project
**1. Load the Dataset**
     ```bash
     from datasets import load_dataset
     dataset = load_dataset("conll2003")

**2. Prepare Data for spaCy**

   Convert the CoNLL-2003 dataset into spaCy’s training format.

**3. Train the Model**
     
   import spacy
   nlp = spacy.load("en_core_web_sm")
   Disable other pipelines and train NER model


**4. Save and Evaluate the Model**
      
   nlp.to_disk("/path/to/save/model")

**5. Run NER on New Headlines**
     
   def perform_ner(text, nlp):
       doc = nlp(text)
       return [(ent.text, ent.label_) for ent in doc.ents]


## **Project Structure**

- **NLP_01.ipynb**: Jupyter notebook with the code and step-by-step process.
- **README.md**: Project documentation.
- **trained_model/**: Directory where the trained spaCy model is saved.

## **Results and Insights**

- **Overall Accuracy**: The model shows strong performance, especially in identifying the most common entity classes.

- **Limitations**: The model can be improved to detect less frequent and complex entities.

## **Future Improvements**
- Experiment with different NER models or architectures to improve classification of less common entities.
- Fine-tune hyperparameters and consider using data augmentation for better generalization.

### **Contact**
For any questions, reach out at aydanrzyv@gmail.com.
