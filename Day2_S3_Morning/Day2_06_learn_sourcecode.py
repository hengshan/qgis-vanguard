import pandas
import inspect

source_DF = inspect.getsource(pandas.DataFrame)
print(type(source_DF))

source_file_DF = inspect.getsourcefile(pandas.DataFrame)
print(source_file_DF)