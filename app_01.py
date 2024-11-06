import streamlit as st
import spacy
from spacy import displacy
from io import StringIO

# Load the trained spaCy model
@st.cache_resource
def load_model(model_path):
    return spacy.load(model_path)

# Path to your trained model
model_path = "C:/Users/Lenovo/Desktop/NER/trained_spacy_model"

# Load the model
try:
    nlp = load_model(model_path)
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

# Title and description of the Streamlit app
st.title("Named Entity Recognition (NER)")
st.markdown("This app performs Named Entity Recognition using a trained spaCy model. Enter text or upload a file to see identified entities.")

# Sidebar for additional options
st.sidebar.header("Settings")
display_mode = st.sidebar.selectbox("Display Mode", ["Entity Labels", "Entity Text with Labels"])
color_option = st.sidebar.checkbox("Highlight Colors", value=True, help="Highlight entities in different colors based on type.")

# Text input for user to enter a headline or sentence
st.subheader("Enter Text for NER")
text = st.text_area("Enter a headline or sentence for NER:", placeholder="Type your text here...")

# Button to analyze the text
if st.button("Analyze Text"):
    if text:
        doc = nlp(text)

        # Define options for displacy rendering, only include 'colors' if color_option is False
        render_options = {} if color_option else {"colors": {}}

        # Display entities using spaCy's displacy renderer
        if display_mode == "Entity Labels":
            html = displacy.render(doc, style="ent", jupyter=False, options=render_options)
            st.write("### Identified Entities")
            st.components.v1.html(html, height=500, scrolling=True)
        else:
            entities = [(ent.text, ent.label_) for ent in doc.ents]
            st.write("### Identified Entities")
            for entity, label in entities:
                st.write(f"**{entity}** ({label})")

        # Option to download the results
        result = "\n".join(f"{ent.text} ({ent.label_})" for ent in doc.ents)
        st.download_button("Download Entities as Text File", data=result, file_name="entities.txt")
    else:
        st.warning("Please enter a text to analyze.")

# Option to upload a text file
st.subheader("Or Upload a Text File for NER")
uploaded_file = st.file_uploader("Choose a text file", type=["txt"])
if uploaded_file:
    # Read and decode file
    text = StringIO(uploaded_file.read().decode("utf-8")).read()
    st.write("File content:", text)

    # Analyze uploaded text
    if text:
        doc = nlp(text)
        
        # Define options for displacy rendering, only include 'colors' if color_option is False
        render_options = {} if color_option else {"colors": {}}

        if display_mode == "Entity Labels":
            html = displacy.render(doc, style="ent", jupyter=False, options=render_options)
            st.write("### Identified Entities from File")
            st.components.v1.html(html, height=500, scrolling=True)
        else:
            entities = [(ent.text, ent.label_) for ent in doc.ents]
            st.write("### Identified Entities from File")
            for entity, label in entities:
                st.write(f"**{entity}** ({label})")

        # Option to download the results
        result = "\n".join(f"{ent.text} ({ent.label_})" for ent in doc.ents)
        st.download_button("Download Entities as Text File", data=result, file_name="entities.txt")



