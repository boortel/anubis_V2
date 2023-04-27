from base.base_trainer import BaseTrainer
from base.base_dataset import BaseADDataset
from base.base_net import BaseNet
from sklearn.metrics import roc_auc_score

import logging
import time
import torch
import torch.optim as optim
import numpy as np
import copy


class AETrainer(BaseTrainer):

    def __init__(self, optimizer_name: str = 'adam', lr: float = 0.001, n_epochs: int = 150, lr_milestones: tuple = (),
                 batch_size: int = 128, weight_decay: float = 1e-6, device: str = 'cuda', n_jobs_dataloader: int = 0):
        super().__init__(optimizer_name, lr, n_epochs, lr_milestones, batch_size, weight_decay, device,
                         n_jobs_dataloader)

    def train(self, dataset: BaseADDataset, ae_net: BaseNet):
        logger = logging.getLogger()

        # Set device for network
        ae_net = ae_net.to(self.device)

        # Get train data loader
        train_loader, _ = dataset.loaders(batch_size=self.batch_size, num_workers=self.n_jobs_dataloader)

        if hasattr(dataset, "validation_set"):
            validation_loader = dataset.val_loader(batch_size=self.batch_size, num_workers=self.n_jobs_dataloader)
            best_auc = 0
            
        # Set optimizer (Adam optimizer for now)
        optimizer = optim.Adam(ae_net.parameters(), lr=self.lr, weight_decay=self.weight_decay,
                               amsgrad=self.optimizer_name == 'amsgrad')

        # Set learning rate scheduler
        scheduler = optim.lr_scheduler.MultiStepLR(optimizer, milestones=self.lr_milestones, gamma=0.1)

        # Training
        logger.info('Starting pretraining...')
        start_time = time.time()
        
        for epoch in range(self.n_epochs):
            ae_net.train()
            loss_epoch = 0.0
            n_batches = 0
            epoch_start_time = time.time()
            
            for data in train_loader:
                inputs, _, _ = data
                inputs = inputs.to(self.device)

                # Zero the network parameter gradients
                optimizer.zero_grad()
                # Update network parameters via backpropagation: forward + backward + optimize
                outputs = ae_net(inputs)
                #inputs = inputs.unsqueeze(-1)
                #print(outputs - inputs)
                scores = torch.sum((outputs - inputs) ** 2, dim=tuple(range(1, outputs.dim())))
                loss = torch.mean(scores)
                loss.backward()
                optimizer.step()

                loss_epoch += loss.item()
                n_batches += 1

            # log epoch statistics
            epoch_train_time = time.time() - epoch_start_time
            logger.info('  Epoch {}/{}\t Time: {:.3f}\t Loss: {:.8f}'
                        .format(epoch + 1, self.n_epochs, epoch_train_time, loss_epoch / n_batches))

            # validation
            if hasattr(dataset, "validation_set"):
                val_start_time = time.time()
                idx_label_score = []
                ae_net.eval()
                with torch.no_grad():
                    for data in validation_loader:
                        inputs, labels, idx = data
                        inputs = inputs.to(self.device)
            
                        outputs = ae_net(inputs)
                        
                        #inputs = inputs.unsqueeze(-1)
                        scores = torch.sum((outputs - inputs) ** 2, dim=tuple(range(1, outputs.dim())))
                        loss = torch.mean(scores)
                        idx_label_score += list(zip(idx.cpu().data.numpy().tolist(),
                                                    labels.cpu().data.numpy().tolist(),
                                                    scores.cpu().data.numpy().tolist()))

                val_train_time = time.time() - val_start_time
                _, labels, scores = zip(*idx_label_score)
                labels = np.array(labels)
                scores = np.array(scores)

                val_auc = roc_auc_score(labels, scores)
                # if get better results save it
                if val_auc > best_auc:
                    ae_net_dict = copy.deepcopy(ae_net.state_dict())
                    best_auc = val_auc
                    ep = epoch + 1
                    
                # log epoch statistics
                logger.info('  Epoch {}/{}\t Time: {:.3f}\t AUC on val_dataset: {:.2f}'
                        .format(epoch + 1, self.n_epochs, val_train_time, val_auc*100.))
            scheduler.step()
            if epoch+1 in self.lr_milestones:
                logger.info('  LR scheduler: new learning rate is %g' % float(scheduler.get_lr()[0]))

        pretrain_time = time.time() - start_time
        logger.info('Pretraining time: %.3f' % pretrain_time)
        
        if hasattr(dataset, "validation_set"):
            logger.info('Restore best weights from Epoch {}/{} AUC: {:.2f}'.format(ep,self.n_epochs,best_auc*100.))
            state_dict = ae_net.state_dict()
            state_dict.update(ae_net_dict)
            ae_net.load_state_dict(state_dict)
            
        logger.info('Finished pretraining.')

        return ae_net

    def test(self, dataset: BaseADDataset, ae_net: BaseNet):
        logger = logging.getLogger()

        # Set device for network
        ae_net = ae_net.to(self.device)

        # Get test data loader
        _, test_loader = dataset.loaders(batch_size=self.batch_size, num_workers=self.n_jobs_dataloader)

        # Testing
        logger.info('Testing autoencoder...')
        loss_epoch = 0.0
        n_batches = 0
        start_time = time.time()
        idx_label_score = []
        ae_net.eval()
        with torch.no_grad():
            for data in test_loader:
                inputs, labels, idx = data
                inputs = inputs.to(self.device)
                outputs = ae_net(inputs)
                
                #inputs = inputs.unsqueeze(-1)
                scores = torch.sum((outputs - inputs) ** 2, dim=tuple(range(1, outputs.dim())))
                loss = torch.mean(scores)

                # Save triple of (idx, label, score) in a list
                idx_label_score += list(zip(idx.cpu().data.numpy().tolist(),
                                            labels.cpu().data.numpy().tolist(),
                                            scores.cpu().data.numpy().tolist()))

                loss_epoch += loss.item()
                n_batches += 1

        logger.info('Test set Loss: {:.8f}'.format(loss_epoch / n_batches))

        _, labels, scores = zip(*idx_label_score)
        labels = np.array(labels)
        scores = np.array(scores)

        auc = roc_auc_score(labels, scores)
        logger.info('Test set AUC: {:.2f}%'.format(100. * auc))

        test_time = time.time() - start_time
        logger.info('Autoencoder testing time: %.3f' % test_time)
        logger.info('Finished testing autoencoder.')
