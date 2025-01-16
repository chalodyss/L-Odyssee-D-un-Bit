# Copyright © 2025 Charles Theetten
# Tous droits réservés.
# Ce programme est distribué sous licence CC BY-NC-ND 4.0.

################################################################################

""" data """

################################################################################

from    sklearn.pipeline    import Pipeline

import  pandas              as pd

################################################################################

class Data:
    """ Data class """

    INITIAL_DATA = None

    def __init__(self, file):
        """ constructor """
        if __class__.INITIAL_DATA is None:
            __class__.INITIAL_DATA = pd.read_csv(file)
        self.df     = __class__.INITIAL_DATA.copy()
        self.df_nan = __class__.INITIAL_DATA.isna()

    ################################################################################

    def build_dataset(self, transformers):
        """ build_dataset function """
        pipeline    = Pipeline(steps = transformers)
        self.df     = pipeline.fit_transform(self.df)

    ################################################################################

    def change_type_columns(self, columns, new_type):
        """ change_type_columns function """
        for col in columns:
            self.df[col] = self.df[col].astype(new_type)

    ################################################################################

    def convert_to_datetime(self, col):
        """ convert_to_datetime function """
        self.df[col] = pd.to_datetime(self.df[col])

    ################################################################################

    def delete_columns(self, columns):
        """ delete_columns function """
        df = self.df.copy()
        return df.drop(columns, axis = 1)

    ################################################################################

    def describe_columns(self, columns):
        """ describe_columns function """
        print(columns.describe())

    ################################################################################

    def display_basic_info(self, n):
        """ display_basic_info function"""
        print(f"Shape : {self.df.shape}.\n")
        print(f"Info  : {self.df.info()}.\n")
        print(self.df.head(n))

    ################################################################################

    def display_nan_info(self):
        """ display_nan_info function """
        p = self.df_nan.sum().sum() / (self.df_nan.shape[0] * self.df_nan.shape[1]) * 100
        print(f"\nMissing values percentage : {p:.2f}%.")
