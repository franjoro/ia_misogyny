from ai.main import ai


def main():
    # TODO: Esto también se podría mejorar
    ai("label", 'train.csv')
    ai("category1", 'train_category1.csv')
    ai("category2", 'train_category2.csv')
    ai("category3", 'train.csv')
    ai("category4", 'train.csv')
    ai("single", 'train.csv')
    ai("groups", 'train.csv')


if __name__ == '__main__':
    main()
