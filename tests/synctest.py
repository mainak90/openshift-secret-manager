from unittest import TestCase
from unittest.mock import patch, Mock
from src.sync import Sync

class TestSync(TestCase):
    @patch('src.sync.Sync')
    def test_sync(self, MockSync):
        Sync = MockSync()
        Sync.checkForSync.return_value = ['Secret-one', 'Secret-two', 'Secret-three']
        output = Sync.checkForSync()
        self.assertIsNone(output)
        self.assertIsInstance(output, list)
        self.assertEqual(output, ['Secret-one', 'Secret-two', 'Secret-three'])

if __name__ == '__main__':
    unittest.main()
