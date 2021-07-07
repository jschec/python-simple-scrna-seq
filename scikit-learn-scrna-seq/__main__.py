from dask.distributed import Client, LocalCluster
from .src import CellMetaData, ExpressionMatrix, SCDataSet, SCRNASeqPipeline
from os.path import dirname, realpath, join
import sys
#import joblib


cluster = LocalCluster()
client = Client(cluster)

CURR_DIR = dirname(realpath(__file__))
PARENT_DIR = dirname(CURR_DIR)
CSV_PATH = join(PARENT_DIR, "data", "metadata.csv")
MATRIX_PATH = join(PARENT_DIR, "data", "matrix.csv")

test_class = CellMetaData(CSV_PATH, "sample_name")
test_matrix = ExpressionMatrix(MATRIX_PATH)
sc_dataset = SCDataSet(test_matrix, sample_annot=test_class)

pipeline = SCRNASeqPipeline(sc_dataset)
pipeline.normalize_expression()

#with joblib.parallel_backend('dask'):
#    grid_search.fit(X, y)