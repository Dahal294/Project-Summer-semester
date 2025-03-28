# Automating Systematic Literature Review : A Clustering based Visual Approach for Efficient Knowledge Synthesis

## Overview
This project introduces a **clustering-based visualization pipeline** to streamline the screening process in **Systematic Literature Reviews (SLRs)**. It addresses the challenges posed by the **exponential growth of research articles** and the **manual effort required** for literature screening.

Using **hierarchical clustering and topic modeling**, the system automatically organizes research papers into meaningful clusters and presents them through **interactive visualizations** such as foam-trees and dendrograms. This enables researchers to explore literature efficiently and reduces the time and effort required for manual screening.

## Features
- **Automated Literature Organization**: Uses clustering techniques to group similar research papers.
- **Interactive Visualizations**: Foam-tree and dendrogram views for better exploration.
- **Faster Screening Process**: Reduces manual effort in literature reviews.
- **Integration**: Can be integrated with other research tools.

## Setup

1. **Download Bio Word Vector**  
   Download the model from [here](https://figshare.com/articles/dataset/Improving_Biomedical_Word_Embeddings_with_Subword_Information_and_MeSH_Ontology/6882647) and save the file inside the `models/` folder.

2. **Install Dependencies**  
   Run the following command to install required libraries:
   ```bash
   pip install -r requirements.txt
   ```
   Or install manually all the required dependencies. 

3. **Run the Code**  
   After setting up, run the script with:
   ```bash
   python main.py
   ```

## Frontend

This project also has a separate frontend repository. To integrate with the frontend, please refer to the [https://github.com/kmiqbal19/Cluster-Visualization-FE].

## Folder Structure
```
/your-project-folder
    /models
        bio_embedding_extrinsic.txt  <-- The model file
    main.py
    requirements.txt (optional)
```

---

## Contributors
- Darpan Dahal – darpan.dahal@st.ovgu.de
- K.M. Iqbal – k.iqbal@st.ovgu.de
- Rajesh Bhandari – rajesh.bhandari@st.ovgu.de


