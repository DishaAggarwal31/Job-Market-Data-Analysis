from data_preprocessing.clean_data import *
from data_preprocessing.merge_data import *

print('Starting the preprocessing of files....')
preprocessing_main()
print('Merging the data files...')
merge_csv_files('data/cleaned/', 'merged_data_jobs.csv')
print('Completed!. Thanks')