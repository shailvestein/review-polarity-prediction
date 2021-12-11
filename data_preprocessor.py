import re
import contractions

punctuation = """
!"#$%&'()*+, -/:;<=>?@[\]^_`{|}~—“”
"""

def remove_text_with_brackets(row):
    row=re.sub("\(.*?\)","",row)
    row=re.sub("\{.*?\}","",row)
    row=re.sub("\[.*?\]","",row)
    row=re.sub("\<.*?\>","",row)
    return row

def remove_stopwords(row):
    doc = ' '.join([word for word in row.split() if word not in stopword])
    return doc

def remove_punctuations(row):
    for punc in punctuation:
        row = row.replace(punc, ' ')
    return row

def remove_digits(row):
    doc = ' '.join([word for word in row.split() if word.isalpha()])
    return doc

def remove_urls(row):
    doc = []
    for word in row.split():
        if not word.startswith('http') and not word.startswith('www'):
            if not len(word)<=2 and not len(word)>12:
                doc.append(word)
    return ' '.join(doc)


def preprocess(row):
    row = str(row)
    row = remove_digits(row)
    row = row.lower()
    decontracted_word_sentences = ' '.join([contractions.fix(word) for word in row.split(' ')])
    row = decontracted_word_sentences.strip()
    row = remove_text_with_brackets(row)
    # row = remove_stopwords(row)
    row = remove_urls(row)
    row = remove_punctuations(row)
    doc = ' '.join([word for word in row.split()])
    
    return doc

####################################################################################################
####################################################################################################
