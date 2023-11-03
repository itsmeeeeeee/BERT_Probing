# BERT_Probing
# Die benötigten Tools, um das Projekt zum Laufen zu bringen
1. Python 3.11.3
2. Jupyter Notebook
3. pandas==2.0.3
4. beautifulsoup4==4.12.2
5. numpy==1.25.0
6. nltk==3.8.1
7. spacy==3.5.4
8. transformers==4.33.3
9. huggingface-hub==0.17.3
10. matplotlib

## Data Extrahieren
# Erste Schritt (Ausführen "data_extraction.py")

Um Daten zu extrahieren und die relevanten Informationen im CSV-Format zu speichern, sollte zuerst die Python-Datei "data_extraction.py" ausgeführt werden. Diese Datei nimmt als Eingabe die ursprünglichen .coref Dateien von OntoNotes Release 5.0 und erzeugt als Ausgabe eine CSV-Datei namens "all_data_fin1.csv". Die Ausgabedatei beinhaltet sieben Spalten: "doc_no", "text_part_no", "Sentence#", "Word", "POS", "coref_id" und "antecedent" .

## Data Labeln
# Zweite Schritt (Ausführen "data_annotation_endlabels.ipynb")

In diesem Schritt werden vier zusätzliche Spalten hinzugefügt: "hypernyms", "labels" (mit den Werten animate/inanimate/other_pos/pronomen), "end_labels" (mit den Werten 0/1/2) und "row Sätze", um sicherzustellen, dass jedes Wort eigene Satzstruktur zugeordnet ist. Das Skript "data_annotation_endlabels.ipynb" nimmt als Eingabe die im ersten Schritt erstellte Datei "all_data_fin1.csv" und erzeugt als Ausgabe die Datei "final_endlabels_with_sentences_word_count.csv"

## Emmbedding Extraction 
# Dritte Schritt (Ausführen `extract_embedding_2m.ipynb`, `extract_embedding_4m.ipynb` und `extract_embedding_6m.ipynb`)

Um Embedding-Vektoren für jedes Wort extrahieren zu können, sollte man die drei Dateien ausführen: `extract_embedding_2m.ipynb`, `extract_embedding_4m.ipynb` und `extract_embedding_6m.ipynb`. Die drei Dateien erhalten als Input den im zweiten Schritt hergestellten Output "final_endlabels_with_sentences_word_count.csv". Aufgrund der großen Datenmenge, die durch wiederholte Sätze im Dataframe entsteht, wurden die ersten zwei Millionen Datensätze für die Datei `extract_embedding_2m.ipynb` verwendet, die zweiten zwei Millionen für `extract_embedding_4m.ipynb` und die letzten zwei Millionen für `extract_embedding_6m.ipynb`. Die drei Dateien sind in Google Colab implementiert, wobei ein Prozessor mit 500 Einheiten zum Einsatz kommt. Als Ausgabe liefern die drei Dateien jeweils `embedding_1_2000000.csv`, `embedding_2_2000000.csv` und `embedding_3_2000000.csv`, die anschließend in `extract_embedding_6m.ipynb` konkateniert und in der Datei `concat_all_embedding_data.csv` gespeichert werden. Diese Datei wird dann als Input für die Probing-Architektur verwendet.

## Probing Architektur (Ausführe "probing_task.ipynb")

In dieser Datei sind zwei Probing-Architekturen implementiert: die logistische Regression und ein Custom Neural Network Netzwerk. Es werden die Metriken beider Probing-Architekturen dargestellt. Zudem erfolgt eine Analyse der korrekt vorhergesagten Pronomen im Vergleich zu Nomen sowie eine Untersuchung der von BERT-Tokenizer in Subwörter segmentierten, vorhergesagten Wörter. Das Script nimmt als Eingabe die im dritten Schritt erstellte Datei "concat_all_embedding_data.csv". 




