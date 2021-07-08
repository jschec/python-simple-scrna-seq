from sklearn.pipeline import Pipeline
from dask_ml.preprocessing import StandardScaler
from dask_ml.decomposition import PCA
from dask_ml.impute import SimpleImputer
import dask.dataframe as dd
#import umap
from .data_sources import SCDataSet

class SCRNASeqPipeline():

    def __init__(self, data_src: SCDataSet) -> None:
        self.__data_src = data_src

    @property
    def data(self) -> SCDataSet:
        return self.__data_src

     # TODO - implement
    def normalize_expression(self, num_dim=100) -> None:
        transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='mean')),
            ('scaler', StandardScaler()),
            ('pca', PCA(n_components=num_dim))
        ])
        test = transformer.fit_transform(self.__data_src.expression_matrix.data)
        print(test)

    # TODO - implement
    def remove_batch_effects(self) -> None:
        pass

    # TODO - implement
    def reduce_dimensions(self, type: str) -> None:
        #X_embedded = TSNE(n_components=2).fit_transform(X)
        pass

    # TODO - implement
    def cluster_cells(self) -> None:
        pass

    # TODO - implement
    def differential_gene_expression(self) -> None:
        pass