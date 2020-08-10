import torch
from torch import mode
import torch.nn as nn
import sys
sys.path.append('.')

from models.util import get_norm
from models.weight_init import weights_init_classifier, weights_init_kaiming

class BNHead(nn.Module):
    def __init__(self, in_features, out_features, bias_freeze, bn_where='after', pooling_size=1):
        assert bn_where in ['before', 'after'], 'bn_where must be before or after'
        super(BNHead, self).__init__()
        self.bn_where = bn_where
        
        if bn_where == 'before':
            self.bnneck = get_norm(in_features, '2d',  bias_freeze)
        else:
            self.bnneck = get_norm(out_features, '1d',  bias_freeze)
        
        self.linear = nn.Linear(in_features * pooling_size * pooling_size, out_features)

        self.linear.apply(weights_init_classifier)
        self.bnneck.apply(weights_init_kaiming)
    
    def forward(self, x):
        if self.bn_where == 'before':
            x = self.bnneck(x)
            x = x.view(x.size(0), -1)
            x = self.linear(x)
        elif self.bn_where == 'after':
            x = x.view(x.size(0), -1)
            x = self.linear(x)
            x = self.bnneck(x)
        return x

    
if __name__ == "__main__":
    model1 = BNHead(2048, 26, False, 'before')

    batch = torch.rand((4, 2048, 1, 1))
    out1 = model1(batch)