import pandas as pd
import re
import unidecode
import nltk
import warnings
import os
import json
import pickle
from nltk.corpus import stopwords
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import mlflow

# Filter specific warning category
warnings.filterwarnings("ignore", category=DeprecationWarning)
nltk.download('stopwords') 
nltk.download('punkt')
main_folder = os.getcwd() 
folder = os.getcwd()+'/RESTAURANTS'
os.chdir(folder)
df = pd.concat([pd.read_csv(file) for file in os.listdir() if '.csv' in file], axis=0)
df = df[(df.tripadv_rating.notnull())]
"""
Some plotting, not necessary for training the model. Only for data understanding.
df.tripadv_rating.value_counts().reindex(np.linspace(1,5,9)).plot(kind='bar')
plt.show()
"""
def preprocess_list(x):
 text_list=x.replace("[","").replace("]","").split(", '")
 for index, text in enumerate(text_list):
   text_list[index] = text.replace("'","")
 return text_list

def preprocess_text(text: str, remove_stopwords: bool) -> str:
    """Function that cleans the input text:
    - remove links
    - remove special characters
    - remove numbers
    - remove stopwords
    - convert to lowercase
    - remove excessive white spaces
    Arguments:
        text (str): text to clean
        remove_stopwords (bool): whether to remove stopwords
    Returns:
        str: cleaned text
    """
    # remove links
    text = re.sub(r"http\S+", "", text)
    # remove numbers and special characters
    #text = re.sub(r"...\S+", "", text)
    # remove stopwords
    if remove_stopwords:
        # 1. create tokens
        tokens = nltk.word_tokenize(text)
        # 2. check if it's a stopword
        tokens = [w.lower().strip() for w in tokens if not w.lower() in stopwords.words("portuguese") and len(w.lower().strip())>2]
        # return a list of cleaned tokens
        return tokens


df['reviews'] = df['reviews'].map(lambda x: preprocess_list(x))
df['price/food/meals/description'] = df['price/food/meals/description'].map(lambda x: preprocess_list(x))
df.reviews.iloc[0]
df['price/food/meals/description'].iloc[1]
df['description'] = df['price/food/meals/description'].map(lambda x: x[1:] if 'R$' in x[0] else x)
df['len'] = df.description.map(lambda x:len(x))
df = df[df.len!=0]
lista= df.description.tolist()

from itertools import chain
flat_list = list(chain(*lista))
if 'R$' in ' '.join(flat_list):
    print(False)
else:
    print(True)

df['price'] = df['price/food/meals/description'].map(lambda x: x[0] if  'R$' in x[0] else None)
df['description'] = df['price/food/meals/description'].map(lambda x: x[1:] if 'R$' in x[0] else x)
df['len'] = df.description.map(lambda x:len(x))
df = df[df.len!=0]
df['minimum_price'] = df.price.map(lambda x: x.split(' - ')[0].replace('R$','').strip() if x!=None else x)
df['maximum_price'] = df.price.map(lambda x: x.split(' - ')[1].replace('R$','').strip() if x!=None else x)

data = df.description.tolist()

def treat_process(x):
    datum=re.sub(r'[...,!,:,),(,*0-9]',' ',unidecode.unidecode(' '.join(','.join(x).split(',')).strip().lower()))   
    return ' '.join(list(set(datum.split(' '))-set(stopwords.words("portuguese"))-set([''])))

df['description'] = df.description.map(lambda x: treat_process(x))
df['reviews'] = df.reviews.map(lambda x: treat_process(x))
df = df[((df.description!='') & (df.description!='...'))]
df['corpus'] = df['description']+df['reviews']
text_data = df.description.tolist()
tag = df.tripadv_rating.tolist()
tagb = df["Unnamed: 0"].tolist()
assert len(tag)==len(text_data)
assert len(tagb)==len(text_data)

os.chdir(main_folder)
dictionary_tag={5:'A', 4.5:'A', 4.0:'B', 3.5:'B',  3.0:'C', 2.5:'C', 2.0:'C', 1.5:'C',1.0:'C',0.5:'C', 0:'C'}
json.dump(df.corpus.tolist(),open('test','w'))
sentences = json.load(open('test','r'))
tagged_documents = [TaggedDocument(doc.split(), [i]) for i, doc in enumerate(sentences)]


# Start an MLflow run
mlflow.start_run()
# Train the Doc2Vec model
vector_size = 300
window = 5
min_count = 1
epochs = 1000
workers = 4
model = Doc2Vec(vector_size=vector_size, window=window, min_count=min_count, workers=workers)
model.build_vocab(tagged_documents)
model.train(tagged_documents, total_examples=model.corpus_count, epochs=epochs)
# Save the model using pickle
model_path = "doc2vec_model.pkl"

with open(model_path, "wb") as f:
    pickle.dump(model, f)

# Log the model as an artifact using MLflow
mlflow.log_artifact(model, artifact_path="models")
# End the MLflow run
mlflow.end_run()

""" This part is about graphical plots/understanding, not really used for the model/deploy.
It consists of recuding the dimensionality of the problem through PCA and TSNE and plot the
result to notice the possible emergence of non-trivial patterns.


from sklearn.manifold import TSNE
from sklearn.decomposition import PCA 

#df['number_of_reviews']=df['number_of_reviews'].map(lambda x: x.split(' ')[0].replace('.','') if isinstance(x,str) \
#                                                    else x).astype(float)


#sns.distplot(df.number_of_reviews[df.number_of_reviews<500])
#def reduce_dimensions(model):
#    num_components = 2  # number of dimensions to keep after compression

    # extract vocabulary from model and vectors in order to associate them in the graph
#    keys = model.dv.index_to_key
#    vectors = np.asarray([model.dv[keys[key]] for key in keys]) 

#    tsne = TSNE(n_components=num_components, random_state=0)
#    pca = PCA(n_components=2)
    
#    vectors_pca = pca.fit_transform(vectors)
#    vectors_tsne = tsne.fit_transform(vectors)

#    x_pca = [v[0] for v in vectors_pca]
#    y_pca = [v[1] for v in vectors_pca]
#    x_tsne = [v[0] for v in vectors_tsne]
#    y_tsne = [v[1] for v in vectors_tsne]
#    labels = [tagb[key] for key in keys]
#    return x_pca, y_pca, x_tsne, y_tsne, labels

#x_pca, y_pca, x_tsne, y_tsne, labels = reduce_dimensions(model)

#plt.scatter(x_pca, y_pca, label = labels)
#plt.show()


#plt.scatter(x_tsne, y_tsne, label = labels)
#plt.show()
"""



