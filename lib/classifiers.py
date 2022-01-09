from imblearn.under_sampling import RandomUnderSampler
from imblearn.over_sampling import RandomOverSampler
from imblearn.pipeline import Pipeline


# This is a classifying function 
def simple_classification(model, X_train, y_train, X_test, y_test):
    fitted_model = model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    test_acc = fitted_model.score(X_test, y_test)
    train_acc =  fitted_model.score(X_train, y_train)
    return train_acc, test_acc, y_pred

# This is a classifier that deals with dataset imbalance by over and then under sampling 
def classification_with_random_sampling(model, X_train, y_train, X_test, y_test):
    over = RandomOverSampler(sampling_strategy="not majority", random_state= 42)
    under = RandomUnderSampler(sampling_strategy= "all")
    steps = [('o', over), ('u', under), ('model', model)]
    pipeline = Pipeline(steps=steps)
    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)
    scores_test = pipeline.score(X_test, y_test)
    scores_train = pipeline.score(X_train, y_train)

    return scores_train, scores_test, y_pred 