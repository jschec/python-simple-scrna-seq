from sklearn.pipeline import Pipeline
#from sklearn.model_selection import train_test_split
#from sklearn.preprocessing import StandardScaler
#from sklearn.impute import SimpleImputer
#from sklearn.decomposition import PCA
from dask_ml.preprocessing import StandardScaler
#from sklearn.compose import ColumnTransformer
#from sklearn.manifold import TSNE
from pandas import pd
import dask.dataframe as dd
#from matplotlib import pyplot as plt
#import umap

class Preprocessor():
    def __init__(self, num_transf: list, cat_transf: list, num_feat: list, cat_feat: list) -> None:
        # maybe put try catch statements here
        self.__numeric_transformer = Pipeline(steps=num_transf)
        self.__categorical_transformer = Pipeline(steps=cat_transf)
        
        self.__numeric_features = num_feat
        self.__categorical_features = cat_feat
    
    @property
    def numeric_transformer(self) -> Pipeline:
        return self.__numeric_transformer

    @property
    def categorical_transformer(self) -> Pipeline:
        return self.__categorical_transformer

    @property
    def numeric_features(self) -> list:
        return self.__numeric_features

    @property
    def categorical_features(self) -> list:
        return self.__categorical_features

    def construct(self) -> ColumnTransformer:
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', self.__numeric_transformer, self.__numeric_features),
                ('cat', self.__categorical_transformer, self.__categorical_features)
            ])
        return preprocessor

def plot_explained_variance():
    # Create a PCA instance: pca
    pca = PCA(n_components=100)
    principalComponents = pca.fit_transform(X_std)
    # Plot the explained variances
    features = range(pca.n_components_)
    plt.bar(features, pca.explained_variance_ratio_, color='black')
    plt.xlabel('PCA features')
    plt.ylabel('variance %')
    plt.xticks(features)
    plt.savefig('foo.png')
    plt.clf()
    # Save components to a DataFrame
    PCA_components = pd.DataFrame(principalComponents)

class SCRNASeqPipeline():

    def __init__(self, data_source) -> None:
        self.__data_source = None

    def scale_expression_matrix(self) -> None:
        numeric_transformer = Pipeline(steps=[
            #('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())
        ])


    # TODO - implement
    def remove_batch_effects(self) -> None:
        pass

    # TODO - implement
    def normalize_cells(self) -> None:
        pass

    # TODO - implement
    def reduce_dimensions(self) -> None:
        pass

    # TODO - implement
    def cluster_cells(self) -> None:
        pass

    # TODO - implement
    def differential_gene_expression(self) -> None:
        pass

def reduce_dim_tsne():
    X = np.array([[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 1]])
    X_embedded = TSNE(n_components=2).fit_transform(X)
    X_embedded.shape

def reduce_dim_umap():
    reducer = umap.UMAP()
    embedding = reducer.fit_transform(X)
    embedding.shape
    plt.scatter(
        embedding[:, 0],
        embedding[:, 1],
        c=[sns.color_palette()[x] for x in penguins.species_short.map({"Adelie":0, "Chinstrap":1, "Gentoo":2})]
        )
    plt.gca().set_aspect('equal', 'datalim')
    plt.title('UMAP projection of the Penguin dataset', fontsize=24)


# create
# how to store meta data?
# umap or tsne for linear 
# cluster cells (which algo to use?)
# differential gene expression
# trajectory analysis
# dask integration?
# plotly? save to html and inject for viewing interactively or should 
# we re-run analysis each time


from sklearn.ensemble import RandomForestClassifier
rf = Pipeline(steps=[('preprocessor', preprocessor),
                      ('classifier', RandomForestClassifier())])