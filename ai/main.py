from ai.data import Data
from ai.model import score_on_model, prediction
import numpy as np
import csv
from sklearn.metrics import confusion_matrix
import seaborn as sn
import matplotlib.pyplot as plt


def k_fold_mean_score(x_train_sets, y_train_sets, x_test_sets, y_test_set, model):

    print("Model: " + model)
    final_confusion_matrix = [[0, 0], [0, 0]]
    scores = []
    for x_train, y_train, x_test, y_test in zip(x_train_sets, y_train_sets, x_test_sets, y_test_set):
        x_train, x_test = Data.train_test_vectors(
            x_train, x_test, [3000, 0.4], "TFIDF")
        y_pred = prediction(x_train, y_train, x_test, model)
        tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
        final_confusion_matrix[0][0] += tn
        final_confusion_matrix[0][1] += fp
        final_confusion_matrix[1][0] += fn
        final_confusion_matrix[1][1] += tp
        scores.append(score_on_model(x_train, y_train, x_test, y_test, model))

    avg = np.mean(scores, axis=0)

    print("Score for train: " + str(avg[0]))
    print("Score for test: " + str(avg[1]))
    print(final_confusion_matrix)

    plt.figure(figsize=(10, 7))
    plt.title(model)
    sn.heatmap(final_confusion_matrix, annot=True,
               fmt='g', linewidths=10, cmap="YlGnBu")
    plt.savefig('./plots/confusion_matrix_' + model)


def write_submission(y_pred, submission_file, column):

    rows = []
    index = 2900

    for y in y_pred:
        rows.append([index, y])
        index += 1

    with open(submission_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["id", column])
        writer.writerows(rows)


def ai(column, path):
    # Crear objeto data
    data = Data('./data/'+path, './data/test2.csv', column)
    # # normalizar cada tweet
    data.preprocess_data()
    x_train_sets, y_train_sets, x_test_sets, y_test_set = data.k_fold_train_test_sets()

    k_fold_mean_score(x_train_sets, y_train_sets,
                      x_test_sets, y_test_set, "LogisticRegression")

    x_train, x_test = Data.train_test_vectors(
        data.TRAIN_DF.text, data.TEST_DF.text, [3000, 0.4], "TFIDF")

    # TODO: Es probable que esto se pueda refactorizar, por ahora así deberia de funcionar
    if(column=="label"):
        y_train = data.TRAIN_DF.label
    elif(column=="category1"):
        y_train = data.TRAIN_DF.category1
    elif(column=="category2"):
        y_train = data.TRAIN_DF.category2
    elif(column=="category3"):
        y_train = data.TRAIN_DF.category3
    elif(column=="category4"):
        y_train = data.TRAIN_DF.category4
    elif(column=="category5"):
        y_train = data.TRAIN_DF.category5
    elif(column=="single"):
        y_train = data.TRAIN_DF.single
    elif(column=="groups"):
        y_train = data.TRAIN_DF.groups
    else:
        raise Exception("Invalid column: "+column)
    print("Predictions for: " + column)

    print("Predictions for the LogisticRegression Model")
    y_pred = prediction(x_train, y_train, x_test, "LogisticRegression")

    write_submission(y_pred, "./submissions/lr_submission_"+column+".csv", column)
    #write_submission(y_pred, "./submissions/lr_submission_.csv", column) Descomentar SOLO si los archivos no se sobreescriben y comentar la linea de arriba.
