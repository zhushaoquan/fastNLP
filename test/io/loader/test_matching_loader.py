
import unittest

from fastNLP.io import DataBundle
from fastNLP.io.loader.matching import RTELoader
from fastNLP.io.loader.matching import QNLILoader
from fastNLP.io.loader.matching import SNLILoader
from fastNLP.io.loader.matching import QuoraLoader
from fastNLP.io.loader.matching import MNLILoader
import os

@unittest.skipIf('TRAVIS' in os.environ, "Skip in travis")
class TestMatchingDownload(unittest.TestCase):
    def test_download(self):
        for loader in [RTELoader, QNLILoader, SNLILoader, MNLILoader]:
            loader().download()
        with self.assertRaises(Exception):
            QuoraLoader().load()

    def test_load(self):
        for loader in [RTELoader, QNLILoader, SNLILoader, MNLILoader]:
            data_bundle = loader().load()
            print(data_bundle)


class TestMatchingLoad(unittest.TestCase):
    def test_load(self):
        data_set_dict = {
            'RTE': ('test/data_for_tests/io/RTE', RTELoader, (5, 5, 5), True),
            'SNLI': ('test/data_for_tests/io/SNLI', SNLILoader, (5, 5, 5), False),
            'QNLI': ('test/data_for_tests/io/QNLI', QNLILoader, (5, 5, 5), True),
            'MNLI': ('test/data_for_tests/io/MNLI', MNLILoader, (5, 5, 5, 5, 6), True),
        }
        for k, v in data_set_dict.items():
            path, loader, instance, warns = v
            if warns:
                with self.assertWarns(Warning):
                    data_bundle = loader().load(path)
            else:
                data_bundle = loader().load(path)

            self.assertTrue(isinstance(data_bundle, DataBundle))
            self.assertEqual(len(instance), data_bundle.num_dataset)
            for x, y in zip(instance, data_bundle.iter_datasets()):
                name, dataset = y
                self.assertEqual(x, len(dataset))

