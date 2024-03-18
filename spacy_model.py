"""
This file contains the model for Spacy to assign entities to strings in our dataset.
We.are.pirates. Bum-ba-dum, dum-dum-dum-dum.
"""

__author__ = "Deryk Clary, Julia MacDonald, Michael Galvan, and MaryGrace Burke"
__credits__ = ["Deryk Clary", "Julia Macdonald", "Michael Galvan", "Mary Grace Burke"]
__email__ = ["deryk.clary@nps.edu", "julia.macdonald@np.edu", "michael.galvan@nps.edu", "mary.burke@nps.edu"]
__status__ = "Development"

# Import modules
import numpy as np
import spacy
from spacy.matcher import Matcher


def generate_matcher(nlp):
    """
    This function creates a matcher based on rules painstakingly trained by trial and error.
    Reference: https://www.youtube.com/watch?v=4V0JDdohxAk
    :param nlp: Initialized spaCy Natural Language Processing model
    :return: Rule-based Matcher object with pre-built rules
    """

    # Create matcher object
    matcher = Matcher(nlp.vocab)

    # Create boarded patterns
    boarded_pattern = [
        {"LOWER": {"NOT_IN": ["police", "guard", "officers", "authority", "personnel", "attempting", "alongside"]}},
        {"LOWER": {"NOT_IN": ["police", "guard", "officers", "authority", "personnel", "to"]}},
        {"POS": "VERB", "LOWER": {"FUZZY": "boarded"}}]
    boarded_pattern2 = [{"LOWER": {"IN": ["knives"]}},
                        {"LOWER": "onboard"}]
    boarded_pattern3 = [{'LEMMA': {"IN": ['seize']}}]  # Lemmas of seize
    boarded_pattern4 = [{"LOWER": {"IN": ["unknown"]}, "OP": "?"},  # Example: 'unknown person escaped'
                        {"LEMMA": {"IN": ["person", "robber", "perpetrator"]}},
                        {"LEMMA": "escape"}]
    boarded_pattern5 = [{"LEMMA": {"IN": ["spot"]}},  # Example: 'spotted # pirates'
                        {"LIKE_NUM": True},
                        {"LEMMA": {"IN": ["pirate"]}}]
    boarded_pattern6 = [{"LEMMA": {"IN": ["robber", "pirate", "thief", "perpetrator"]}},  # Example: 'pirates escaped'
                        {"LEMMA": {"IN": ["steal", "disembark"]}}]
    boarded_pattern7 = [{"LEMMA": {"IN": ["manage", "climb"]}},  # Example: 'managed to climb/escape'
                        {"IS_ALPHA": True, "OP": "?"},
                        {"LOWER": {"IN": ["climb", "board", "escape"]}}]
    boarded_pattern8 = [{"LOWER": {"IN": ["climbed"]}},  # Example: 'climbed on board'
                        {"IS_ALPHA": True, "OP": "?"},
                        {"LOWER": "board"}]
    boarded_pattern9 = [{"LEMMA": {"IN": ["robber", "pirate", "thief", "perpetrator"]}},  # Example: 'robbers on board'
                        {"LOWER": {"IN": ["were", "on"]}, "OP": "?"},
                        {"LEMMA": "board"},
                        {"LOWER": {"NOT_IN": ["attempted"]}, "OP": "?"}]
    boarded_pattern10 = [{"LEMMA": "board"},  # Example: 'on board were pirates'
                         {"IS_ALPHA": True, "OP": "?"},
                         {"LEMMA": {"IN": ["robber", "pirate", "thief", "perpetrator"]}}]
    boarded_pattern11 = [{"LEMMA": {"IN": ["robber", "pirate", "thief", "perpetrator"]}, "OP": "?"},
                         # Example: robbers jumped overboard
                         {"LEMMA": {"IN": ["break", "jump"]}},
                         {"LOWER": {"IN": ["into", "overboard"]}}]
    boarded_pattern12 = [{"LOWER": {"IN": ["lock", "door"]}},
                         {"LOWER": "was", "OP": "?"},  # Example: lock was broken
                         {"LEMMA": "break"}]
    boarded_pattern13 = [{"LOWER": "on"},  # Example: pirates on board barge
                         {"LEMMA": "board"},
                         {"LOWER": "barge"}]
    boarded_pattern14 = [{"LEMMA": {"IN": ["robber", "pirate", "thief", "perpetrator"]}},
                         # Example: robbers were sighted in
                         {"LOWER": "were"},
                         {"LOWER": "sighted"},
                         {"LOWER": "in"}]
    boarded_pattern15 = [{"LOWER": "boarded", "IS_SENT_START": True}]
    boarded_pattern16 = [{"LEMMA": 'steal'},
                         {"LOWER": 'mooring'}]
    boarded_pattern17 = [{"LOWER": "on"},
                         {"LOWER": "the"},
                         {"LOWER": "stern"}]

    # Hijack patterns
    hijack_pattern = [{'LEMMA': 'hijack'}]  # Token's lemma is 'hijack'
    hijack_pattern2 = [{'LEMMA': 'seize'},  # Token pattern: 'seize control'
                       {'LOWER': 'control'}]

    # Hostage/crew assaulted patterns
    hostage_pattern = [{'LEMMA': {'IN': ['abduct', 'kidnap', 'hostage']}}]  # Lemmas: abduct, kidnap, hostage
    crew_assault_pattern = [{'LEMMA': 'assault'}]

    # Add patterns to matcher with associated categories
    matcher.add('BOARDED', [boarded_pattern, boarded_pattern2, boarded_pattern3, boarded_pattern4, boarded_pattern5,
                            boarded_pattern6, boarded_pattern7, boarded_pattern8, boarded_pattern9,
                            boarded_pattern10, boarded_pattern11, boarded_pattern12, boarded_pattern13,
                            boarded_pattern14, boarded_pattern15, boarded_pattern16, boarded_pattern17,
                            hijack_pattern, hijack_pattern2, hostage_pattern])
    matcher.add('HIJACKED', [hijack_pattern, hijack_pattern2])
    matcher.add('HOSTAGES_TAKEN', [hostage_pattern])
    matcher.add('CREW_ASSAULTED', [crew_assault_pattern])

    # Return resulting matcher object
    return matcher


def custom_matcher(data_df, docs, matcher):
    """
    Takes the dataframe, Doc objects, and matcher, and puts all the data into the dataframe.
    :param data_df: Dataframe to store all the match data
    :param docs: Doc objects for all the strings in a column of the dataframe
    :param matcher: Matcher object initialized with preset rules (see generate_matcher)
    :return: Completed dataframe with all matches places into the columns as binary
    """
    for ix, doc in enumerate(docs):
        # Get matches in the doc and extract the found tags' strings
        matches = matcher(doc)
        matches_str = [doc.vocab.strings[x[0]] for x in matches]

        # Add all matches found into matched_df
        data_df.at[ix, 'BOARDED'] = np.where('BOARDED' in matches_str, 1, 0)
        data_df.at[ix, 'HIJACKED'] = np.where('HIJACKED' in matches_str, 1, 0)
        # Below are commented out because the matcher isn't trained to handle them yet
        # training_data.at[ix,'HOSTAGES_TAKEN'] = np.where('HOSTAGES_TAKEN' in matches_str, 1, 0)
        # training_data.at[ix,'CREW_ASSAULTED'] = np.where('CREW_ASSAULTED' in matches_str, 1, 0)

    return data_df


def apply_nlp(text, nlp):
    """
    Apply the NLP to each text that is passed to the function from the apply function
    :param text: Text to be tested for categories
    :param nlp: NLP object that identifies categories
    :return: Tuple with (was boarded, was hijacked, hostages, assault)
    """
    doc = nlp(text)

    boarded = hijacked = hostages = assault = 0

    for span in doc.spans['sc']:
        if span.label_ == 'BOARDED':
            boarded = 1
        if span.label_ == 'HIJACKED':
            hijacked = 1
        if span.label_ == 'HOSTAGES_TAKEN':
            hostages = 1
        if span.label_ == 'CREW_ASSAULTED':
            assault = 1

    return boarded, hijacked, hostages, assault


def model_interpreter(data_df, column_name, nlp):
    """
    Function to apply the NLP model to the specified column.
    Puts the results in new columns in the Dataframe
    :param data_df: Dataframe with data to test
    :param column_name: (String) Column name that you'd like to test
    :param nlp: NLP to categorize the data
    :return: Dataframe with hijacked and boarded columns based on what the model found.
    """
    # Apply passed nlp to specified column, put resulting tuple in result column
    data_df['RESULT'] = data_df[column_name].apply(apply_nlp, args=[nlp])

    # Split results into their associated columns
    data_df['BOARDED'] = np.where(data_df['RESULT'].str[0] == 1, 1, 0)
    data_df['HIJACKED'] = np.where(data_df['RESULT'].str[1] == 1, 1, 0)
    data_df['HOSTAGES_TAKEN'] = np.where(data_df['RESULT'].str[2] == 1, 1, 0)
    data_df['CREW_ASSAULTED'] = np.where(data_df['RESULT'].str[3] == 1, 1, 0)

    # Drop results column
    data_df.drop(columns=['RESULT'], axis=1, inplace=True)

    # Return resulting df
    return data_df


def style(s, bold=False):
    """
    Style dependencies for html_generator method below.
    Reference: https://www.youtube.com/watch?v=4V0JDdohxAk
    """
    blob = f"<text>{s}</text>"
    if bold:
        blob = f"<b style='background-color: #fff59d'>{blob}</b>"
    return blob


def html_generator(g, matcher, n=10):
    """
    Generate HTML representation of all the matches found in a Document object.
    Highlights all matches based on the Matcher object.
    :param g: String to be represented
    :param matcher: Matcher object to find all matches that w
    :param n: Number of entries to show/print
    :return: Blob to print
    """
    blob = ""
    for i in range(n):
        doc = next(g)

        state = [[t, False] for t in doc]
        for idx, start, end in matcher(doc):
            for i in range(start, end):
                state[i][1] = True
        blob += style(' '.join([style(str(t[0]), bold=t[1]) for t in state]) + '<br>')
    return blob
