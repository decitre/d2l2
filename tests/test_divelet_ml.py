import numpy as np
import pytest

import divelet_ml as d2l


def test_array_loader_covers_every_row_once():
    X, y = np.arange(10).reshape(5, 2), np.arange(5)
    for shuffle in (False, True):
        loader = d2l.ArrayLoader((X, y), batch_size=2, shuffle=shuffle)
        batches = list(loader)
        assert len(loader) == len(batches) == 3 and len(batches[-1][0]) == 1
        rows = np.concatenate([b[1] for b in batches])
        assert sorted(rows) == list(range(5))
        assert all((bX[:, 0] // 2 == by).all() for bX, by in batches)  # X and y rows stay paired
    assert [b[1].tolist() for b in d2l.ArrayLoader((X, y), 2)] == [[0, 1], [2, 3], [4]]
    dropped = d2l.ArrayLoader((X, y), 2, drop_last=True)
    assert len(dropped) == 2 and [b[1].tolist() for b in dropped] == [[0, 1], [2, 3]]


def test_save_hyperparameters():
    class Data(d2l.DataModule):
        def __init__(self, a, b=2, _hidden=3):
            super().__init__()
            self.save_hyperparameters()

    data = Data(1)
    assert (data.a, data.b) == (1, 2) and not hasattr(data, '_hidden')
    assert data.hparams == {'a': 1, 'b': 2}


def test_add_to_class():
    class A:
        pass

    @d2l.add_to_class(A)
    def double(self, x):
        return 2 * x

    assert A().double(3) == 6


def test_data_module_dataloaders():
    data = d2l.DataModule()
    assert data.hparams == {'root': '../data', 'num_workers': 4}
    with pytest.raises(NotImplementedError):
        data.train_dataloader()

    class Data(d2l.DataModule):
        def get_dataloader(self, train):
            return 'train' if train else 'val'

    assert (Data().train_dataloader(), Data().val_dataloader()) == ('train', 'val')
