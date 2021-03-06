# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/models.ipynb (unless otherwise specified).

__all__ = ['Flatten', 'gem', 'GeM', 'SnapModel']

# Cell
import torch
import torch.nn as nn
import torchvision
import torch.nn.functional as F

from torch.nn.parameter import Parameter

# Cell
class Flatten(nn.Module):
    "Flatten `x` to a single dimension, often used at the end of a model. `full` for rank-1 tensor"
    def __init__(self, full:bool=False):
        super().__init__()
        self.full = full
    def forward(self, x): return x.view(-1) if self.full else x.view(x.size(0), -1)

# Cell
def gem(x, p=3, eps=1e-6):
    return F.avg_pool2d(x.clamp(min=eps).pow(p), (x.size(-2), x.size(-1))).pow(1./p)

class GeM(nn.Module):
    def __init__(self, p=3, eps=1e-6):
        super(GeM,self).__init__()
#         self.p = Parameter(torch.ones(1)*p).cuda()
        self.p = Parameter(torch.ones(1)*p)
        self.eps = eps
    def forward(self, x):
        return gem(x, p=self.p, eps=self.eps)
    def __repr__(self):
        return self.__class__.__name__ + '(' + 'p=' + '{:.4f}'.format(self.p.data.tolist()[0]) + ', ' + 'eps=' + str(self.eps) + ')'

# Cell
class SnapModel(nn.Module):
    def __init__(self, pretrained=True):
        super(SnapModel, self).__init__()
        model = torchvision.models.resnet50(pretrained=pretrained)
        extras = [GeM(), Flatten()]
        self.model = nn.Sequential(*(list(model.children())[:-2] + extras))

    def forward(self, x):
        out = self.model(x)
#         return torch.norm(out, dim=0)
        return out