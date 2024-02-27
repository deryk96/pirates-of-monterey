"""
This file contains the model for Spacy to assign entities to strings in our dataset.
We.are.pirates. Bum-ba-dum, dum-dum-dum-dum.
"""

__author__ = "Deryk Clary, Julia MacDonald, Michael Galvan, and MaryGrace Burke"
__credits__ = ["Deryk Clary", "Julia Macdonald", "Michael Galvan", "Mary Grace Burke"]
__email__ = ["deryk.clary@nps.edu", "julia.macdonald@np.edu", "michael.galvan@nps.edu", "mary.burke@nps.edu"]
__status__ = "Development"

# Import modules
import spacy


def model_training(docs, nlp):
    """
    This function trains the model for assigning entities to docs within the dataset.
    Reference: https://course.spacy.io/en/chapter4
    :param docs: Set of docs containing
    :param nlp: Natural Language Processing instance
    :return: Model trained on the docs
    """

    # Set up matcher
    matcher = spacy.Matcher(nlp.vocab)

    # Boarded pattern
    boarded_patterns = [{'LOWER': 'board'}]
    matcher.add("boarded", boarded_patterns)

    # Generate matches
    for doc in docs:
        matches = matcher(doc)
        spans = [spacy.Span(doc, start, end, label=match_id)
                 for match_id, start, end in matches]
        doc.ents = spans
        docs.append(doc)

    # Save the model
    doc_bin = spacy.DocBin(docs=docs)
    doc_bin.to_disk("./train.spacy")


def relevant_chunks(doc):
    for chunk in doc.noun_chunks:
        if chunk.root.head.lemma_ in ['buy', 'purchase']:  # Replace with relevant verbs
            if chunk.rood.dep_ == 'dobj':
                yield chunk

def model_tester(doc, nlp):
    """
    This function prints out all matches for a given doc.
    :param doc: A single Spacy doc
    :return: None
    """

    # Displays a nice rendered display of matching tokens
    spacy.displacy.render(doc, style='ent')

    # Iterate through all matches and view traits
    for match_id, start, end in doc:
        span = doc[start:end]
        string_id = nlp.vocab.strings[match_id]
        print(match_id, start, end, span.text, string_id)
