import sys
sys.path.append('.')

import torch
import torch.nn as nn
import torch.nn.functional as F

class Singular_BCE(nn.Module):
    def __init__(self, num_attribute, reduction='sum'):
        super(Singular_BCE, self).__init__()
        assert reduction in ['sum', 'mean', 'attribute']
        self.reduction = 'mean' if reduction == 'attribute' else reduction
        self.num_attribute = num_attribute if reduction == 'attribute' else 1

    def forward(self, logits, targets, idx_attribute):
        return F.binary_cross_entropy_with_logits(logits.gather(1, idx_attribute.unsqueeze(1)).squeeze(), targets.gather(1, idx_attribute.unsqueeze(1)).squeeze(), reduction=self.reduction)*self.num_attribute

