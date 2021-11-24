from get import get_classes_for_files_columns, get_files_of_size
from map import map_items
from dataset import create_train_test_dataset
from answears import get_correct_answears
from learning import train_and_test_process
from efficiency import get_efficiency

s1 = input("Podaj rozmiar zbioru testowego [0.0-1.0]: ")
s2 = input("Czy wyświetlać szczegóły wyniku końcowego? [tak/nie]: ")

if s2 == 'tak':
    s2 = True
else:
    s2 = False

get_files_of_size()
get_classes_for_files_columns()
map_items()
create_train_test_dataset(float(s1))
get_correct_answears()
train_and_test_process()
get_efficiency(s2)
