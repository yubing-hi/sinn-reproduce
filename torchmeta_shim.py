import torch
from torch import nn
from collections import OrderedDict


class MetaModule(nn.Module):
    """
    Minimal implementation compatible with torchmeta MetaModule.
    Supports passing external parameters during forward.
    """

    def meta_named_parameters(self):
        for name, param in self.named_parameters():
            yield name, param

    def get_subdict(self, params, key):
        if params is None:
            return None
        return OrderedDict(
            (k[len(key)+1:], v) for k, v in params.items() if k.startswith(key)
        )


class MetaSequential(nn.Sequential, MetaModule):
    """
    Sequential container compatible with MetaModule.
    Allows passing params dictionary to submodules.
    """

    def forward(self, input, params=None):
        for name, module in self._modules.items():

            if isinstance(module, MetaModule):
                subdict = None
                if params is not None:
                    subdict = self.get_subdict(params, name)

                input = module(input, params=subdict)
            else:
                input = module(input)

        return input