from pandas.core import series
import dask.dataframe as dd
import dask.array as da
import mimetypes
import os

class MetaData():
    def __init__(self, file_path: str, index_col: str) -> None:
        self.__file_path = file_path
        self.__file_type = mimetypes.guess_type(file_path)
        self._index_col = index_col
        self._data = None

    @property
    def data(self) -> dd:
        return self._data

    @property
    def columns(self) -> list:
        return list(self._data.columns)

    @property
    def nrows(self) -> int:
        return len(self._data.index)

    @property
    def ncols(self) -> int:
        return len(self._data.columns)

    def _load(self) -> None:
        print(self.__file_type)
        self._data = dd.read_csv(self.__file_path)
        self._data.set_index(self._index_col)
        

class GeneMetaData(MetaData):
    def __init__(self, file_path: str, index_col: str):
        super().__init__(file_path, index_col)

    #TODO - confirm return type; will likely have different method body as well
    @property
    def genes(self) -> list:
        return self._data[self._index_col]

class CellMetaData(MetaData):
    def __init__(self, file_path: str, index_col: str):
        super().__init__(file_path, index_col)
        self._load()

    #TODO - confirm return type
    @property
    def cells(self) -> series:
        return self._data[self._index_col].compute()


class ExpressionMatrix():
    
    def __init__(self, file_path: str) -> None:
        self.__file_path = file_path
        self.__file_type = mimetypes.guess_type(file_path)
        self._data = None
        self._load()

    @property
    def data(self) -> da:
        return self._data

    @property
    def nrows(self) -> int:
        pass

    @property
    def ncols(self) -> int:
        pass

    def _load(self) -> None:
        print(self.__file_type)
        print(self.__file_path, os.path.isfile(self.__file_path))
        # read into df in 25MB chunks
        df = dd.read_csv(self.__file_path, blocksize=25e6, sample=1000000)
        print(df.head())
        self._data = df.to_dask_array() #lengths=True


class SCDataSet():

    def __init__(self, expr_matrix: da, sample_annot: dd = None, gene_annot: dd = None) -> None:
        self.__expr_matrix = expr_matrix
        self.__sample_annot = sample_annot
        self.__gene_annot = gene_annot

    @property
    def expression_matrix(self) -> da:
        return self.__expr_matrix

    #TODO - add error
    @expression_matrix.setter
    def expression_matrix(self, new_matrix):
         self.__expr_matrix = new_matrix

    @property
    def cell_meta_data(self) -> dd:
        return self.__sample_annot

    @property
    def gene_meta_data(self) -> dd:
        return self.__gene_annot

    @property
    def genes(self) -> series:
        return self.__gene_annot.genes

    @property
    def samples(self) -> series:
        return self.__gene_annot.samples

    @property
    def expression_matrix_shape(self) -> tuple:
        return (self.__expr_matrix.nrows, self.__expr_matrix.ncols)