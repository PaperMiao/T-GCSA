import torch
import torch.nn as nn

class GCNLayer(nn.Module):
    
    def __init__(self, in_ft, out_ft, act='prelu', bias=True):
        
        super(GCNLayer, self).__init__()
        
        self.fc = nn.Linear(in_ft, out_ft, bias=False)
        self.act = nn.PReLU() if act == 'prelu' else nn.ReLU()
        
        if bias:
            self.bias = nn.Parameter(torch.FloatTensor(out_ft))
            self.bias.data.fill_(0.0)
        else:
            self.register_parameter('bias', None)

        for m in self.modules():
            self.weights_init(m)

    def weights_init(self, m):
        if isinstance(m, nn.Linear):
            torch.nn.init.xavier_uniform_(m.weight.data)
            if m.bias is not None:
                m.bias.data.fill_(0.0)

    def forward(self, seq, adj, sparse=False):
        seq_fts = self.fc(seq)
        if sparse:
            out = torch.unsqueeze(torch.spmm(adj, torch.squeeze(seq_fts, 0)), 0)
        else:
            out = torch.mm(adj, seq_fts)
        if self.bias is not None:
            out += self.bias

        return self.act(out)
    
    
class feat_self_attention(nn.Module):
    
    def __init__(self, in_ft, out_ft, act='prelu', bias=True):
        
        super(feat_self_attention, self).__init__()
        
        self.fc = nn.Linear(in_ft, out_ft, bias=False)
        self.act = nn.PReLU() if act == 'prelu' else nn.ReLU()
        
        if bias:
            self.bias = nn.Parameter(torch.FloatTensor(out_ft))
            self.bias.data.fill_(0.0)
        else:
            self.register_parameter('bias', None)

        for m in self.modules():
            self.weights_init(m)

    def weights_init(self, m):
        if isinstance(m, nn.Linear):
            torch.nn.init.xavier_uniform_(m.weight.data)
            if m.bias is not None:
                m.bias.data.fill_(0.0)
                
    def forward(self, seq, adj, sparse=False):
        
        if sparse:
            out = torch.unsqueeze(torch.spmm(adj, torch.squeeze(seq, 0)), 0)
        else:
            out = torch.mm(adj, seq)
        if self.bias is not None:
            out += self.bias
            
        out = out.t()
        out = self.fc(out)

        return self.act(out)