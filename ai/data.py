import pandas as pd
from sklearn.model_selection import KFold
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from ai.preprocess_data import preprocess_tweet


class Data:

    def __init__(self, path_train, path_test, column):
        self.TRAIN_DF = pd.read_csv(path_train, sep=',')
        self.TEST_DF = pd.read_csv(path_test, sep=',')
        self.x = self.TRAIN_DF.text
        # TODO: Es probable que esto se pueda refactorizar, por ahora así deberia de funcionar
        if(column=="label"):
            self.y = self.TRAIN_DF.label
        elif(column=="category1"):
            self.y = self.TRAIN_DF.category1
        elif(column=="category2"):
            self.y = self.TRAIN_DF.category2
        elif(column=="category3"):
            self.y = self.TRAIN_DF.category3
        elif(column=="category4"):
            self.y = self.TRAIN_DF.category4
        elif(column=="category5"):
            self.y = self.TRAIN_DF.category5
        elif(column=="single"):
            self.y = self.TRAIN_DF.single
        elif(column=="groups"):
            self.y = self.TRAIN_DF.groups
        else:
            raise Exception("Invalid column: "+column)
        print(self.TRAIN_DF.columns)

    def k_fold_train_test_sets(self):
        x_train_sets = []
        x_test_sets = []
        y_train_sets = []
        y_test_sets = []
        kf = KFold(n_splits=10, random_state=50, shuffle=True)
        for train_index, test_index in kf.split(self.x):
            x_train_sets.append(self.x[train_index])
            x_test_sets.append(self.x[test_index])
            y_train_sets.append(self.y[train_index])
            y_test_sets.append(self.y[test_index])

        return x_train_sets, y_train_sets, x_test_sets, y_test_sets

    def preprocess_data(self):
        print(self.TRAIN_DF)
        self.TRAIN_DF.text = self.TRAIN_DF.text.apply(preprocess_tweet)
        self.TEST_DF.text = self.TEST_DF.text.apply(preprocess_tweet)

    @staticmethod
    def train_test_vectors(train, test, param, vec="COUNT"):

        if vec == "COUNT":
            vectorizer = CountVectorizer(
                max_features=param[0], max_df=param[1])
        elif vec == "TFIDF":
            vectorizer = TfidfVectorizer(
                max_features=param[0], max_df=param[1])

        x_train = vectorizer.fit_transform(train)
        x_test = vectorizer.transform(test)

        return x_train, x_test
