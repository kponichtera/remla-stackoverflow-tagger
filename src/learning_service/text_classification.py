"""
Train the model.
"""
import json
import os
import uuid
from typing import List, Any

import pandas as pd
import scipy
from joblib import load, dump
from prometheus_client import Gauge
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import accuracy_score, f1_score, average_precision_score, roc_auc_score
from sklearn.multiclass import OneVsRestClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import FunctionTransformer

from common.bucket import upload_model
from learning_service.config import settings, VarNames
from learning_service.read_data import read_data_from_file

OUTPUT_PATH = settings[VarNames.OUTPUT_DIR.value]

TRAIN_DATA_FILE_PATH = os.path.join(OUTPUT_PATH, "train_preprocessed_data.joblib")
TRAIN_LABELS_FILE_PATH = os.path.join(OUTPUT_PATH, "train_preprocessed_labels.joblib")

VALIDATION_DATA_FILE_PATH = os.path.join(OUTPUT_PATH, "val_preprocessed_data.joblib")
VALIDATION_LABELS_FILE_PATH = os.path.join(OUTPUT_PATH, "val_preprocessed_labels.joblib")

LABEL_PREPROCESSOR = os.path.join(OUTPUT_PATH, "preprocessor_labels.joblib")
DATA_PREPROCESSOR = os.path.join(OUTPUT_PATH, "preprocessor_data.joblib")

ACCURACY_SCORE = Gauge('stackoverflow_tagger_accuracy_score', 'Model accuracy score')
F1_SCORE = Gauge('stackoverflow_tagger_f1_score', 'F1-score')
AVERAGE_PRECISION_SCORE = Gauge('stackoverflow_tagger_average_precision_score', 'Average precision score')
ROC_AUC = Gauge('stackoverflow_tagger_roc_auc', 'Area under the Receiver operating characteristic curve')
LATEST_MODEL_UPDATE = Gauge('stackoverflow_tagger_latest_model_update', 'Unix timestamp of the latest model update time')

def train_classifier(X_train, y_train, penalty='l1', C=1.0):
    """Create and fit LogisticRegression wrapped into OneVsRestClassifier

    Args:
        X_train (_type_): _description_
        y_train (_type_): _description_
        penalty (str, optional): penalty for training, possible values are:
                {'l1', 'l2', 'elasticnet', 'none'}. Defaults to 'l1'.
        C (float, optional): C : Inverse of regularization strength; must be a positive float.
                Like in support vector machines, smaller values specify stronger
                regularization. Defaults to 1.0 .

    Returns:
        OneVsRestClassifier: classifier
    """
    # clf = LogisticRegression(
    #     penalty=penalty,
    #     C=C,
    #     dual=False,
    #     solver='liblinear',
    #     verbose=1,
    #     n_jobs=-1
    # )

    clf = SGDClassifier(
        penalty=penalty,
        max_iter=5000,
        verbose=1,
        n_jobs=-1
    )
    clf = OneVsRestClassifier(clf, n_jobs=-1)
    print("###################### TRAINING ######################")
    clf.fit(X_train, y_train)
    print("####################### DONE #########################")
    return clf


def predict_labels(
    classifier: OneVsRestClassifier,
    input_data: scipy.sparse.csr.csr_matrix or List[str],
    inverse_transformer=None):
    """Predicts labels for given test data.

    Args:
        classifier (OneVsRestClassifier): classifier to make predictions on.
        input_data (scipy.sparse.csr.csr_matrix or List[str]): data for predictions
        inverse_transformer (MultiLabelBinarizer or None, optional): flag determining 
                    if inverse transform is applied to predictions.. Defaults to None.

    Returns:
        scipy.sparse.csr.csr_matrix or List[str]: result of predictions
    """
    test_predictions = classifier.predict(input_data)
    if inverse_transformer is None:
        return test_predictions
    test_pred_inverse = inverse_transformer.inverse_transform(test_predictions)
    return test_pred_inverse


def get_evaluation_scores(
    predicted_labels : scipy.sparse.csr.csr_matrix,
    actual_data : scipy.sparse.csr.csr_matrix,
    actual_labels : scipy.sparse.csr.csr_matrix,
    classifier: Any,
    print_stats=True):
    """Gets evaluation scores for a trained model.

    Args:
        predicted_labels (scipy.sparse.csr.csr_matrix): predicted labels
        actual_labels (scipy.sparse.csr.csr_matrix): test labels
        actual_data (scipy.sparse.csr.csr_matrix): test data
        classifier (Any): trained classifier
        print_stats (bool, optional): flag to determine if evaluation
                                stats will be printed. Defaults to True.

    Returns:
        dict: dictionary of scores
    """
    accuracy_score_num = accuracy_score(actual_labels, predicted_labels)
    f1_score_num = f1_score(actual_labels, predicted_labels, average='weighted')
    precision_score = average_precision_score(actual_labels, predicted_labels, average='macro')
    predicted_scores = classifier.decision_function(actual_data)
    roc_auc_score_num = roc_auc_score(actual_labels, predicted_scores, multi_class='ovo')

    ACCURACY_SCORE.set(accuracy_score_num)
    F1_SCORE.set(f1_score_num)
    AVERAGE_PRECISION_SCORE.set(precision_score)
    ROC_AUC.set(roc_auc_score_num)
    LATEST_MODEL_UPDATE.set_to_current_time()

    if print_stats:
        print('\n############### Evaluation Scores ###############\n')
        print('Accuracy score           :', accuracy_score_num)
        print('F1 score                 :', f1_score_num)
        print('Average precision score  :', precision_score)
        print('ROC curve score          :', roc_auc_score_num)

    return {
        "accuracy_score": accuracy_score_num,
        "f1_score": f1_score_num,
        "average_precision_score": precision_score,
        "roc_auc": roc_auc_score_num,
    }

def retrain_model(classifier):
    pass

def main(bucket_upload=False,
         train_data_file = TRAIN_DATA_FILE_PATH,
         train_labels_file = TRAIN_LABELS_FILE_PATH,
         validation_data_file = VALIDATION_DATA_FILE_PATH,
         validation_labels_file = VALIDATION_LABELS_FILE_PATH,
         classifier = None):
    """Main function run training

    Args:
        bucket_upload (bool, optional): determined if the model should
                be uploaded to a bucket. Defaults to True.
    """
    X_train = load(train_data_file)
    y_train = load(train_labels_file)

    X_val = load(validation_data_file)
    y_val = load(validation_labels_file)

    label_preprocessor = load(LABEL_PREPROCESSOR)

    raw_data = read_data_from_file("validation.tsv")
    raw_titles = raw_data["title"].values

    classifier = train_classifier(X_train, y_train) if classifier is None else classifier.partial_fit(X_train, y_train)
    classifier_name = f'{str(uuid.uuid4())}_model'

    # Non inverse transformed data
    y_val_pred = predict_labels(classifier, X_val)
    y_val_inversed = label_preprocessor.inverse_transform(y_val)

    evaluation_scores = get_evaluation_scores(
        y_val_pred,
        X_val,
        y_val,
        classifier
    )

    with open(
        os.path.join(
            OUTPUT_PATH,
            f"{classifier_name}_evaluation.json"
        ),
        'w',
        encoding='utf-8'
        ) as outfile:
        json.dump(evaluation_scores, outfile, indent=2)
    
    with open(
        os.path.join(
            OUTPUT_PATH,
            "evaluation.json"
        ),
        'w',
        encoding='utf-8'
        ) as outfile:
        json.dump(evaluation_scores, outfile, indent=2)

    # Inverse transformed data
    misclassifications_dict = {
        "title": raw_titles,
        "tags (actual)" : y_val_inversed,
        "tags (predicted)" : label_preprocessor.inverse_transform(y_val_pred)
    }
    df_misclassifications = pd.DataFrame.from_dict(misclassifications_dict)
    filter_func = df_misclassifications["tags (actual)"] != \
        df_misclassifications["tags (predicted)"]
    df_misclassifications = df_misclassifications[filter_func]
    df_misclassifications.to_csv(
        os.path.join(OUTPUT_PATH, f"{classifier_name}_misclassifications.csv")
    )
    # Store "best" classifier
    classifier_pipeline = make_pipeline(
        load(DATA_PREPROCESSOR),
        FunctionTransformer(classifier.predict),
        FunctionTransformer(label_preprocessor.inverse_transform)
    )
    filename = f'{classifier_name}.joblib'
    classifier_filename = f'{classifier_name}_classifier.joblib'
    model_path = os.path.join(OUTPUT_PATH, filename)
    classifier_path = os.path.join(OUTPUT_PATH, classifier_filename)
    dump(classifier_pipeline, model_path)

    dump(classifier, classifier_path)

    if bucket_upload:
        auth = (
            settings[VarNames.OBJECT_STORAGE_ACCESS_KEY.value],
            settings[VarNames.OBJECT_STORAGE_SECRET_KEY.value],
            settings[VarNames.OBJECT_STORAGE_TLS.value]
        )
        upload_model(
            model_path,
            settings[VarNames.BUCKET_NAME.value],
            settings[VarNames.MODEL_OBJECT_KEY.value],
            settings[VarNames.OBJECT_STORAGE_ENDPOINT.value],
            *auth
        )
        upload_model(
            classifier_path,
            settings[VarNames.BUCKET_NAME.value],
            settings[VarNames.CLASSIFIER_OBJECT_KEY.value],
            settings[VarNames.OBJECT_STORAGE_ENDPOINT.value],
            *auth
        )
        upload_model(
            DATA_PREPROCESSOR,
            settings[VarNames.BUCKET_NAME.value],
            settings[VarNames.PREPROCESSOR_DATA_OBJECT_KEY.value],
            settings[VarNames.OBJECT_STORAGE_ENDPOINT.value],
            *auth
        )
        upload_model(
            LABEL_PREPROCESSOR,
            settings[VarNames.BUCKET_NAME.value],
            settings[VarNames.PREPROCESSOR_LABELS_OBJECT_KEY.value],
            settings[VarNames.OBJECT_STORAGE_ENDPOINT.value],
            *auth
        )
        upload_model(
            os.path.join(OUTPUT_PATH, "evaluation.json"),
            settings[VarNames.BUCKET_NAME.value],
            settings[VarNames.STATISTICS_OBJECT_KEY.value],
            settings[VarNames.OBJECT_STORAGE_ENDPOINT.value],
            *auth
        )


if __name__ == "__main__":
    main()
