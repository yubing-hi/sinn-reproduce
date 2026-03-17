import numpy as np
import torch
from torch.utils.data import Dataset

from torch import nn


class model(nn.Module):
    """
    DeGroot 形式: x_u(t+1) = x_u(t) + sum_{v in U\\u} a_uv * x_v(t)，
    即下一时刻 = 当前自身意见 + 其他用户意见的加权和（不含自身）。
    """

    def __init__(self, num_users=1, type='relu',
                 hidden_features=256, num_hidden_layers=3, **kwargs):
        super().__init__()
        self.num_users = num_users
        # a_uv，v≠u 时表示 u 受 v 的影响权重；对角线在计算时置 0
        self.A = nn.Parameter(torch.randn(num_users, num_users) * 0.1)

    def forward(self, model_input):
        # previous: (batch, num_users)，当前时刻各用户意见
        # ui: (batch, 1)，要预测的用户 id
        previous = model_input['previous']
        uids = model_input['ui']
        device = previous.device
        # 只保留 v≠u 的权重，对角线置 0
        A_nd = self.A * (1.0 - torch.eye(self.num_users, device=device))
        # 自身当前意见 x_u(t)
        self_opinion = torch.gather(previous, 1, uids)  # (batch, 1)
        # sum_{v in U\u} a_uv * x_v(t)
        influence = (A_nd[uids[:, 0], :] * previous).sum(dim=-1, keepdim=True)
        output = self_opinion + influence
        output = torch.tanh(output)
        return {'opinion': output}


def loss_function(model_output, gt, loss_definition="MAE"):
    '''
       x: batch of input coordinates
       y: usually the output of the trial_soln function
       '''
    gt_latent_opinion = gt['opinion']
    pred_latent_opinion = model_output['opinion']

    data_loss = (pred_latent_opinion - gt_latent_opinion)**2

    # Exp      # Lapl
    # -----------------
    return {'data_loss': data_loss.mean(), 
           }



