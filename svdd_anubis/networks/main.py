from .lotus_LeNet import LOTUS_LeNet, LOTUS_LeNet_Autoencoder
from .lotus_2conv import LOTUS_2conv, LOTUS_Autoencoder_2conv
from .lotus_4conv import LOTUS_4conv, LOTUS_Autoencoder_4conv
from .lotus_LeNet_single import LOTUS_LeNet_single, LOTUS_LeNet_Autoencoder_single
from .lotus_LeNet_fewer_filters import LOTUS_LeNet_fewer_filters, LOTUS_LeNet_Autoencoder_fewer_filters
from .lotus_LeNet_more_filters import LOTUS_LeNet_more_filters, LOTUS_LeNet_Autoencoder_more_filters
from .mnist_LeNet import MNIST_LeNet, MNIST_LeNet_Autoencoder
from .cifar10_LeNet import CIFAR10_LeNet, CIFAR10_LeNet_Autoencoder
from .cifar10_LeNet_elu import CIFAR10_LeNet_ELU, CIFAR10_LeNet_ELU_Autoencoder

from .my_LeNet import MY_LeNet, MY_LeNet_Autoencoder
from .my_LeNet_480x480 import MY_LeNet_480, MY_LeNet_480_Autoencoder
from .my_LeNet_NN import MY_LeNet_NN, MY_LeNet_NN_Autoencoder


def build_network(net_name, net_res, net_rep_dim):
    """Builds the neural network."""

    implemented_networks = ('lotus_LeNet', 'lotus_LeNet_single', 'lotus_fewer_filters', 'lotus_more_filters', 'lotus_4conv', 'lotus_2conv', 'mnist_LeNet', 'cifar10_LeNet', 'cifar10_LeNet_ELU', 'my_LeNet', 'my_LeNet_480', 'my_LeNet_NN')
    assert net_name in implemented_networks, "Unknown net_name! Available:" + str(implemented_networks)

    net = None
    print(net_name)
    if net_name == 'lotus_LeNet':
        net = LOTUS_LeNet(net_res, net_res, net_rep_dim)
    
    if net_name == 'lotus_LeNet_single':
        net = LOTUS_LeNet_single(net_res, net_res, net_rep_dim)
    if net_name == 'lotus_more_filters':
        net = LOTUS_LeNet_more_filters(net_res, net_res, net_rep_dim)
    if net_name == 'lotus_fewer_filters':
        net = LOTUS_LeNet_fewer_filters(net_res, net_res, net_rep_dim)
    if net_name == 'lotus_2conv':
        net = LOTUS_2conv(net_res, net_res, net_rep_dim)

    if net_name == 'lotus_4conv':
        net = LOTUS_4conv(net_res, net_res, net_rep_dim)


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


def build_autoencoder(net_name, net_res, net_rep_dim):
    """Builds the corresponding autoencoder network."""

    implemented_networks = ('lotus_LeNet', 'lotus_4conv', 'lotus_2conv', 'lotus_more_filters', 'lotus_fewer_filters', 'lotus_LeNet_single', 'mnist_LeNet', 'cifar10_LeNet', 'cifar10_LeNet_ELU', 'my_LeNet', 'my_LeNet_480', 'my_LeNet_NN')
    assert net_name in implemented_networks, "Unknown net_name! Available:" + str(implemented_networks)

    ae_net = None
    
    if net_name == 'lotus_LeNet':
        ae_net = LOTUS_LeNet_Autoencoder(net_res, net_res, net_rep_dim)

    if net_name == 'lotus_fewer_filters':
        ae_net = LOTUS_LeNet_Autoencoder_fewer_filters(net_res, net_res, net_rep_dim)

    if net_name == 'lotus_more_filters':
        ae_net = LOTUS_LeNet_Autoencoder_more_filters(net_res, net_res, net_rep_dim)

    if net_name == 'lotus_LeNet_single':
        ae_net = LOTUS_LeNet_Autoencoder_single(net_res, net_res, net_rep_dim)

    if net_name == 'lotus_2conv':
        ae_net = LOTUS_Autoencoder_2conv(net_res, net_res, net_rep_dim)

    if net_name == 'lotus_4conv':
        ae_net = LOTUS_Autoencoder_4conv(net_res, net_res, net_rep_dim)

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
