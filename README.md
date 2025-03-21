# Bio Word Vector - Biomedical Word Embeddings

This project uses the Bio Word Vector model to improve biomedical word embeddings with subword information and MeSH ontology.

## Setup

1. **Download Bio Word Vector**  
   Download the model from [here](https://figshare.com/articles/dataset/Improving_Biomedical_Word_Embeddings_with_Subword_Information_and_MeSH_Ontology/6882647) and save the file inside the `models/` folder.

2. **Install Dependencies**  
   Run the following command to install required libraries:
   ```bash
   pip install -r requirements.txt
   ```
   Or install manually:
   ```bash
   pip install numpy pandas scipy gensim sklearn
   ```

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

## License

MIT License


