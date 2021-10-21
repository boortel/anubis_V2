from .mnist import MNIST_Dataset
from .cifar10 import CIFAR10_Dataset
from .mydata import MYDATA_Dataset
from .bee import BEE_Dataset


def load_dataset(dataset_name, data_path, normal_class):
    """Loads the dataset."""

    implemented_datasets = ('mnist', 'cifar10', 'mydata100', 'mydata300', 'mydata100HRes',
                            'mydata300HRes', 'mydata100HRes_480', 'mydata300HRes_480', 'bee')
    assert dataset_name in implemented_datasets

    dataset = None

    if dataset_name == 'mnist':
        dataset = MNIST_Dataset(root=data_path, normal_class=normal_class)

    if dataset_name == 'cifar10':
        dataset = CIFAR10_Dataset(root=data_path, normal_class=normal_class)
        
    if dataset_name == 'mydata100':
        dataset = MYDATA_Dataset(root=data_path, normal_class=normal_class, version=100, validation=True)
    
    if dataset_name == 'mydata300':
        dataset = MYDATA_Dataset(root=data_path, normal_class=normal_class, version=300)

    if dataset_name == 'mydata100HRes':
        dataset = MYDATA_Dataset(root=data_path, normal_class=normal_class, version=100, Res=0)
    
    if dataset_name == 'mydata300HRes':
        dataset = MYDATA_Dataset(root=data_path, normal_class=normal_class, version=300, Res=0)
    
    if dataset_name == 'mydata100HRes_480':
        dataset = MYDATA_Dataset(root=data_path, normal_class=normal_class,
                                 version=100, Res=480, validation=False)
    
    if dataset_name == 'mydata300HRes_480':
        dataset = MYDATA_Dataset(root=data_path, normal_class=normal_class,
                                 version=300, Res=480, validation=True)
        
    if dataset_name == 'bee':
        dataset = BEE_Dataset(root=data_path, normal_class=normal_class)
        
    return dataset
