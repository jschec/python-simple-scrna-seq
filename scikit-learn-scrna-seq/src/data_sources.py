from pandas.core import series
import dask.dataframe as dd
import dask.array as da
import mimetypes
import os
import time


class MetaData():
    def __init__(self, file_path: str, index_col: str) -> None:
        self.__file_path = file_path
        self.__file_type = mimetypes.guess_type(file_path)[0]
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

    def _load(self) -> bool:
        if self.__file_type == "text/csv":
            self._data = dd.read_csv(self.__file_path)
        else:
            print(self.__file_type == "text/csv", self.__file_type)
            return False

        self._data.set_index(self._index_col)
        return True
        

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
        load_status = self._load()
        print("CellMetaData load_status:", load_status)

    #TODO - confirm return type
    @property
    def samples(self) -> series:
        return self._data[self._index_col].compute()


class ExpressionMatrix():
    
    def __init__(self, file_path: str) -> None:
        self.__file_path = file_path
        self.__file_type = mimetypes.guess_type(file_path)[0]
        self._data = None
        load_status = self._load()
        print("ExpressionMatrix load_status:", load_status)

    @property
    def data(self) -> da:
        return self._data

    #TODO - add error handling
    @data.setter
    def data(self, new_data):
         self._data = new_data

    @property
    def nrows(self) -> int:
        pass

    @property
    def ncols(self) -> int:
        pass

    def _load(self) -> None:
        if self.__file_type == "text/csv":
            # read into df in 25MB chunks
            print("Reading csv...")
            tic = time.perf_counter()
            df = dd.read_csv(self.__file_path, blocksize=25e6, sample=1000000)
            toc = time.perf_counter()
            print(f"Eclipsed time: {toc - tic:0.4f} seconds")
            print(df.head())
            
            print()
            print("to dask array...")
            tic = time.perf_counter()
            self._data = df.to_dask_array() #lengths=True
            toc = time.perf_counter()
            print(f"Eclipsed time: {toc - tic:0.4f} seconds")

            print()
            print("compute chunk sizes...")
            tic = time.perf_counter()
            self._data.compute_chunk_sizes()
            toc = time.perf_counter()
            print(f"Eclipsed time: {toc - tic:0.4f} seconds")

            print(self._data[0])
            print(self._data.shape)
        else:
            print(self.__file_type == "text/csv", self.__file_type)
            return False

        return True


class SCDataSet():

    def __init__(self, expr_matrix: ExpressionMatrix, sample_annot: CellMetaData = None, gene_annot: GeneMetaData = None) -> None:
        self.__expr_matrix = expr_matrix
        self.__sample_annot = sample_annot
        self.__gene_annot = gene_annot

    @property
    def expression_matrix(self) -> ExpressionMatrix:
        return self.__expr_matrix

    @property
    def cell_meta_data(self) -> CellMetaData:
        return self.__sample_annot

    @property
    def gene_meta_data(self) -> GeneMetaData:
        return self.__gene_annot

    @property
    def genes(self) -> series:
        return self.__gene_annot.genes

    @property
    def samples(self) -> series:
        return self.__sample_annot.samples

    @property
    def expression_matrix_shape(self) -> tuple:
        return (self.__expr_matrix.nrows, self.__expr_matrix.ncols)