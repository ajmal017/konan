import api.broker as broker # konan.api.broker

example_root = 'HOME/DATA/'
example_type = 'json'

# instantiate data broker object
lb = broker.DataBroker(path_root = example_root)

# OPTIONAL: create a general target directory; e.g. used many times, critical file
lb.data_repository.markSpecialDirectory(key = 'MY_DATA',
                                            path_data = example_path)

# access target directory and store in variable
example_path = lb.data_repository.special_directories['MY_DATA']

# store full path to file in variable
# file_name parameters should be wriiten according to data style standards
path_target_data = lb.getLocalData(type_data = example_type,
                                    path_data = example_path,
                                    file_name = 'datestring-or-description')

print path_target_data
