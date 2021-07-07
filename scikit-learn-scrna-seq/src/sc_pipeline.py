#from sklearn.pipeline import Pipeline
from dask_ml.preprocessing import StandardScaler
import dask.dataframe as dd
from .data_sources import SCDataSet

class SCRNASeqPipeline():

    def __init__(self, data_src: SCDataSet) -> None:
        self.__data_src = data_src

    @property
    def data(self) -> SCDataSet:
        return self.__data_src

     # TODO - implement
    def normalize_expression(self) -> None:
        #numeric_transformer = Pipeline(steps=[
        #    ('imputer', SimpleImputer(strategy='median')),
        #    ('scaler', StandardScaler())
        #])
        scaler = StandardScaler()
        self.__data_src.expression_matrix = scaler.transform(self.__data_src.expression_matrix)

    # TODO - implement
    def remove_batch_effects(self) -> None:
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