from get import get_classes_for_files_columns, get_files_of_size
from map import map_items
from dataset import create_train_test_dataset
from answears import get_correct_answears
from learning import train_and_test_process
from efficiency import get_efficiency
from items import get_items_classes

get_files_of_size(20)
#get_items_classes()
get_classes_for_files_columns()
map_items()
create_train_test_dataset()
# get_correct_answears()
train_and_test_process()
get_efficiency()
