import torch
import torch.nn as nn


class TimmModel(nn.Module):
    def __init__(self, name, pretrained=True):
        super(TimmModel, self).__init__()
        import timm

        self.feature_extractor = timm.create_model(name, pretrained=pretrained)

        self.feature_dim = self.feature_extractor.forward_features(
            torch.randn(2, 3, 256, 128)
        ).size(1)

    def forward(self, x):
        return self.feature_extractor.forward_features(x)

    def get_feature_dim(self):
        return self.feature_dim
