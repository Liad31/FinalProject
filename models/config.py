# config.py

class Config(object):
    embed_size = 100
    hidden_layers = 1
    hidden_size = 32
    bidirectional = True
    output_size = 1
    max_epochs = 15
    lr = 0.5
    batch_size = 2
    dropout_keep = 0.5
    max_sen_len = 30 # Sequence length for RNN