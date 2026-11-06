"""d2l2's NumPy counterpart of the `d2l` library, imported as `import d2l2 as d2l`.

`add_to_class`, `HyperParameters` and `DataModule` are adapted from D2L's `d2l/torch.py`
(https://github.com/d2l-ai/d2l-en, commit 23d7a5aecceee57d1292c56e90cce307f183bb0a),
Copyright 2019 Amazon.com, Inc. or its affiliates, MIT-0 license (LICENSE-SAMPLECODE).
Only what adapted chapters use is here.
"""

import inspect

import numpy as np


def add_to_class(Class):
    """Register functions as methods in created class."""
    def wrapper(obj):
        setattr(Class, obj.__name__, obj)
    return wrapper


class HyperParameters:
    """The base class of hyperparameters."""
    def save_hyperparameters(self, ignore=[]):
        """Save function arguments into class attributes."""
        frame = inspect.currentframe().f_back
        _, _, _, local_vars = inspect.getargvalues(frame)
        self.hparams = {k: v for k, v in local_vars.items()
                        if k not in set(ignore + ['self']) and not k.startswith('_')}
        for k, v in self.hparams.items():
            setattr(self, k, v)


class DataModule(HyperParameters):
    """The base class of data."""
    def __init__(self, root='../data', num_workers=4):
        self.save_hyperparameters()

    def get_dataloader(self, train):
        raise NotImplementedError

    def train_dataloader(self):
        return self.get_dataloader(train=True)

    def val_dataloader(self):
        return self.get_dataloader(train=False)


class ArrayLoader:
    """Minibatches of NumPy arrays, in place of a framework's data loader such as PyTorch's `DataLoader`.

    Iterating yields tuples of `batch_size` rows of each array. The last batch is smaller when
    `batch_size` doesn't divide the number of rows, or left out with `drop_last=True`.
    With `shuffle=True`, the rows are in a new random order on every pass.
    """
    def __init__(self, arrays, batch_size, shuffle=False, drop_last=False):
        assert len({len(a) for a in arrays}) == 1, 'arrays must have the same number of rows'
        self.arrays, self.batch_size, self.shuffle, self.drop_last = arrays, batch_size, shuffle, drop_last

    def __len__(self):
        n = len(self.arrays[0])
        return n // self.batch_size if self.drop_last else -(-n // self.batch_size)

    def __iter__(self):
        n = len(self.arrays[0])
        order = np.random.permutation(n) if self.shuffle else np.arange(n)
        for i in range(0, len(self) * self.batch_size, self.batch_size):
            batch = order[i:i + self.batch_size]
            yield tuple(a[batch] for a in self.arrays)
