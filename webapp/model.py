from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
import pickle
import joblib


def svm_model(text):
    svm_from_joblib = joblib.load('webapp/model/svm.pkl')
    result = svm_from_joblib.predict([text])[0]
    return result