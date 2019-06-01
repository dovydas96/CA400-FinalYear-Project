from pathlib import Path
import pandas as pd
from PIL import Image
from torch.utils.data import Dataset


class DeepFashionDatasetFactory:
    """Deep Fashion Dataset Factory"""

    def __init__(self, root_dir, eval_partition_file, category_file):
        """
        Args:
            root_dir (string): Path to images
            eval_partition_file (string): Feather file of partitions
            category_file (string): Feather file of categories
        """
        self.root_dir = Path(root_dir)
        self.eval_partition = (
            pd.read_csv(eval_partition_file).set_index('image_name')
        )
        self.categories = (
            pd.read_csv(category_file).set_index('image_name')
        )

    def create_dataset(self, eval_status, transform=None):
        """
        Args:
            eval_status (string): one of train, val, test
            transform (callable, optional): Transform to be called on a sample
        """
        return DeepFashionDataset(self.root_dir, eval_status,
                                  self.eval_partition, self.categories,
                                  transform)


class DeepFashionDataset(Dataset):
    """Deep Fashion Dataset"""

    def __init__(self, root_dir, eval_status, eval_partition, categories,
                 transform=None):
        """
        Args:
            root_dir (Path): Path to images
            eval_status (pd.DataFrame): one of
            eval_partition (pd.DataFrame): DataFrame of partitions
            categories (pd.DataFrame): DataFrame of categories
            transform (callable, optional): Transform to be called on a sample
        """
        self.root_dir = root_dir
        self.eval_status = eval_status
        self.eval_partition = eval_partition
        self.categories = categories
        self.transform = transform
        matching_eval = self.eval_partition == eval_partition
        self.train_idx = list(self.eval_partition[matching_eval].index)

    def __len__(self):
        return len(self.train_idx)

    def __getitem__(self, idx):
        img_name = self.root_dir / self.train_idx[idx]
        query_image = Image.open(img_name)
        category = self.eval_partition.loc[self.train_idx[idx]].values[0]
        anchor = {'image': query_image, 'category_name': category}
        if self.transform:
            anchor = self.transform(anchor)
        return (anchor[0], anchor[1])

    def sample(self, idx):
        im = self.train_idx[idx]
        category = self.eval_partition.loc[self.train_idx[idx]].values[0]
        return im, category

    @property
    def classes(self):
        return self.categories['category_name'].values
