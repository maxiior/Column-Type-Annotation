from get import get_classes_for_files_columns, get_files_of_size
from map import map_items
from dataset import create_train_test_dataset
from learning import train_and_test_process
from efficiency import get_efficiency
from items import get_items_classes

s1 = input("Podaj rozmiar zbioru testowego [0.0-1.0]: ")
s2 = input("Czy wyświetlać szczegóły wyniku końcowego? [tak/nie]: ")

if s2 == 'tak':
    s2 = True
else:
    s2 = False

a = input("Czy pobrać nowe dane? [tak/nie]: ")

if a == 'tak':
    s3 = input("Podaj maksymalną ilość wierszy w pliku: ")
    get_files_of_size(s3)
    get_items_classes()

get_classes_for_files_columns()
map_items()
create_train_test_dataset(float(s1))
train_and_test_process()
get_efficiency(s2)
