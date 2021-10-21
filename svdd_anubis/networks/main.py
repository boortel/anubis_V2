from .mnist_LeNet import MNIST_LeNet, MNIST_LeNet_Autoencoder
from .cifar10_LeNet import CIFAR10_LeNet, CIFAR10_LeNet_Autoencoder
from .cifar10_LeNet_elu import CIFAR10_LeNet_ELU, CIFAR10_LeNet_ELU_Autoencoder

from .my_LeNet import MY_LeNet, MY_LeNet_Autoencoder
from .my_LeNet_480x480 import MY_LeNet_480, MY_LeNet_480_Autoencoder
from .my_LeNet_NN import MY_LeNet_NN, MY_LeNet_NN_Autoencoder


def build_network(net_name):
    """Builds the neural network."""

    implemented_networks = ('mnist_LeNet', 'cifar10_LeNet', 'cifar10_LeNet_ELU', 'my_LeNet', 'my_LeNet_480', 'my_LeNet_NN')
    assert net_name in implemented_networks

    net = None

    if net_name == 'mnist_LeNet':
        net = MNIST_LeNet()

    if net_name == 'cifar10_LeNet':
        net = CIFAR10_LeNet()

    if net_name == 'cifar10_LeNet_ELU':
        net = CIFAR10_LeNet_ELU()

    if net_name == 'my_LeNet':
        net = MY_LeNet()
    
    if net_name == 'my_LeNet_480':
        net = MY_LeNet_480()
        
    if net_name == 'my_LeNet_NN':
        net = MY_LeNet_NN()
        
    return net


def build_autoencoder(net_name):
    """Builds the corresponding autoencoder network."""

    implemented_networks = ('mnist_LeNet', 'cifar10_LeNet', 'cifar10_LeNet_ELU', 'my_LeNet', 'my_LeNet_480', 'my_LeNet_NN')
    assert net_name in implemented_networks

    ae_net = None

    if net_name == 'mnist_LeNet':
        ae_net = MNIST_LeNet_Autoencoder()

    if net_name == 'cifar10_LeNet':
        ae_net = CIFAR10_LeNet_Autoencoder()

    if net_name == 'cifar10_LeNet_ELU':
        ae_net = CIFAR10_LeNet_ELU_Autoencoder()

    if net_name == 'my_LeNet':
        ae_net = MY_LeNet_Autoencoder()

    if net_name == 'my_LeNet_480':
        ae_net = MY_LeNet_480_Autoencoder()
    
    if net_name == 'my_LeNet_NN':
        ae_net = MY_LeNet_NN_Autoencoder()
        
    return ae_net
