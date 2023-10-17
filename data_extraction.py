import glob
import re

import pandas as pd
import spacy
from bs4 import BeautifulSoup, NavigableString, ResultSet, Tag

nlp = spacy.load("en_core_web_sm")


def remove_specialCharacter(text):
    # remove the special character
    pattern = re.compile(
        r"\*(?!-?\d+)(?!PRO\*\b)(?!T\b)[A-Z]+\*(?!-?\d+)|\*T|\*PRO|\*|\*EXP|-\d+|\bEXP\b"
    )

    clean_sentence = re.sub(pattern, "", text)
    return clean_sentence

# Extract coref_id
def parse_coref(coref: Tag, id):
    refs = []
    if isinstance(coref, Tag) and len(coref.contents) == 1:
        refs.append((id, coref.text))
        return refs

    if isinstance(coref, NavigableString):
        refs.append((id, coref.text))
        return refs

    for coref in coref.contents:
        if isinstance(coref, NavigableString):
            refs += parse_coref(coref, id)
        else:
            refs += parse_coref(coref, coref.get("id"))
    return refs


def extraxt_file(filename):
    data = []
    ref_ids = {}
    with open(filename, "r", encoding="utf-8") as file:
        content = file.read()
        soup = BeautifulSoup(content, "html.parser")
        tag = soup.find("doc")
        docno = tag.get("docno")

        texts = soup.doc.find_all("text")
        for text in texts:
            # print("text",text)
            texttmp = text
            partno = texttmp.get("partno")
            # print("partnr.........", partno)

            ####################################################
            # sentences = []
            sentence_number = 1

            # Finde alle <text> Elemente
            text_elements: ResultSet[Tag] = soup.find_all("text")
            # print("text_element",text_elements)
            for text_element in text_elements:
                # Extract the text content of the <text> element
                

                html_sentences = text_elements[0].decode_contents().split(".")
                for sentance in html_sentences:
                    el = BeautifulSoup(sentance, "html.parser")
                    for node in el.children:
                        if not node:
                            continue
                        if isinstance(node, NavigableString):
                            doc = nlp(remove_specialCharacter(node.strip()))
                            for token in doc:
                                word = token.text
                                pos = token.pos_
                                # # Create the desired data format
                                data.append(
                                    [
                                        docno,
                                        partno,
                                        sentence_number,
                                        word,
                                        pos,
                                        None,
                                        None,
                                    ]
                                )
                        if isinstance(node, Tag):
                            refs = parse_coref(node, node.get("id"))
                            for id, ref_words in refs:
                                doc = nlp(remove_specialCharacter(ref_words.strip()))
                                for token in doc:
                                    word = token.text
                                    pos = token.pos_
                                    ref_text = (
                                        ref_ids.get(id, None)
                                        if pos == "PRON"
                                        and len(ref_words.split(" ")) == 1
                                        else None
                                    )
                                   
                                    data.append(
                                        [
                                            docno,
                                            partno,
                                            sentence_number,
                                            word,
                                            pos,
                                            id,
                                            ref_text,
                                        ]
                                    )
                                    ref_ids.setdefault(id, ref_words)

                    sentence_number += 1

                
    return data


#files = glob.glob("./*coref")
files=glob.glob("C:/Users/aldi_/Desktop/bachelorarbeit/Dataset/original_data/*coref")


csvdata = [
    ["doc_no", "text_part_no", "Sentence#", "Word", "POS", "coref_id", "antecedent"]
]


resultdata = extraxt_file(files[0])
csvdata += resultdata



#df = pd.DataFrame(csvdata)

#df.to_csv("C:/Users/aldi_/Desktop/bachelorarbeit/Dataset/all_data_csv/all_data_fin1.csv", index=False, header=False)
