import dill
import os
import sys

from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, ExtraTreesRegressor, AdaBoostRegressor, GradientBoostingRegressor, GradientBoostingClassifier, ExtraTreesClassifier, AdaBoostClassifier

from sklearn.linear_model import RandomizedLasso, RandomizedLogisticRegression, RANSACRegressor, LinearRegression, Ridge, Lasso, ElasticNet, LassoLars, OrthogonalMatchingPursuit, BayesianRidge, ARDRegression, SGDRegressor, PassiveAggressiveRegressor, LogisticRegression, RidgeClassifier, SGDClassifier, Perceptron, PassiveAggressiveClassifier

from sklearn.cluster import MiniBatchKMeans

keras_installed = False
try:
    # Suppress some level of logs
    os.environ['TF_CPP_MIN_VLOG_LEVEL'] = '3'
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
    import tensorflow as tf
    tf.logging.set_verbosity(tf.logging.INFO)
    from keras.constraints import maxnorm
    from keras.layers import Dense, Dropout
    from keras.models import Sequential
    from keras.wrappers.scikit_learn import KerasRegressor, KerasClassifier
    keras_installed = True
except:
    pass

from auto_ml import utils


xgb_installed = False
try:
    import xgboost as xgb
    xgb_installed = True
except ImportError:
    pass

lgb_installed = False
try:
    import lightgbm as lgb
    lgb_installed = True
except ImportError:
    pass


def get_model_from_name(model_name, training_params=None):

    # For Keras
    epochs = 250
    if 'is_test_suite' in sys.argv:
        print('Heard that this is the test suite. Limiting epochs to 10, which will increase training speed dramatically at the expense of model accuracy')
        epochs = 10

    all_model_params = {
        'LogisticRegression': {'n_jobs': -2},
        'RandomForestClassifier': {'n_jobs': -2},
        'ExtraTreesClassifier': {'n_jobs': -1},
        'AdaBoostClassifier': {'n_estimators': 10},
        'SGDClassifier': {'n_jobs': -1},
        'Perceptron': {'n_jobs': -1},
        'LinearRegression': {'n_jobs': -2},

        'RandomForestRegressor': {'n_jobs': -2},
        'ExtraTreesRegressor': {'n_jobs': -1},
        'MiniBatchKMeans': {'n_clusters': 8},
        'GradientBoostingRegressor': {'presort': False},
        'SGDRegressor': {'shuffle': False},
        'PassiveAggressiveRegressor': {'shuffle': False},
        'AdaBoostRegressor': {'n_estimators': 10},
        'XGBRegressor': {'nthread':-1, 'n_estimators': 200},
        'XGBClassifier': {'nthread':-1, 'n_estimators': 200},
        'LGBMRegressor': {},
        'LGBMClassifier': {},
        'DeepLearningRegressor': {'epochs': epochs, 'batch_size': 50, 'verbose': 2},
        'DeepLearningClassifier': {'epochs': epochs, 'batch_size': 50, 'verbose': 2}
    }

    model_params = all_model_params.get(model_name, None)
    if model_params is None:
        model_params = {}

    if training_params is not None:
        print('Now using the model training_params that you passed in:')
        print(training_params)
        # Overwrite our stock params with what the user passes in (i.e., if the user wants 10,000 trees, we will let them do it)
        model_params.update(training_params)
        print('After overwriting our defaults with your values, here are the final params that will be used to initialize the model:')
        print(model_params)


    model_map = {
        # Classifiers
        'LogisticRegression': LogisticRegression(),
        'RandomForestClassifier': RandomForestClassifier(),
        'RidgeClassifier': RidgeClassifier(),
        'GradientBoostingClassifier': GradientBoostingClassifier(),
        'ExtraTreesClassifier': ExtraTreesClassifier(),
        'AdaBoostClassifier': AdaBoostClassifier(),


        'SGDClassifier': SGDClassifier(),
        'Perceptron': Perceptron(),
        'PassiveAggressiveClassifier': PassiveAggressiveClassifier(),

        # Regressors
        'LinearRegression': LinearRegression(),
        'RandomForestRegressor': RandomForestRegressor(),
        'Ridge': Ridge(),
        'ExtraTreesRegressor': ExtraTreesRegressor(),
        'AdaBoostRegressor': AdaBoostRegressor(),
        'RANSACRegressor': RANSACRegressor(),
        'GradientBoostingRegressor': GradientBoostingRegressor(),

        'Lasso': Lasso(),
        'ElasticNet': ElasticNet(),
        'LassoLars': LassoLars(),
        'OrthogonalMatchingPursuit': OrthogonalMatchingPursuit(),
        'BayesianRidge': BayesianRidge(),
        'ARDRegression': ARDRegression(),
        'SGDRegressor': SGDRegressor(),
        'PassiveAggressiveRegressor': PassiveAggressiveRegressor(),

        # Clustering
        'MiniBatchKMeans': MiniBatchKMeans()
    }

    if xgb_installed:
        model_map['XGBClassifier'] = xgb.XGBClassifier()
        model_map['XGBRegressor'] = xgb.XGBRegressor()

    if lgb_installed:
        model_map['LGBMRegressor'] = lgb.LGBMRegressor()
        model_map['LGBMClassifier'] = lgb.LGBMClassifier()

    if keras_installed:

        model_map['DeepLearningClassifier'] = KerasClassifier(build_fn=make_deep_learning_classifier)
        model_map['DeepLearningRegressor'] = KerasRegressor(build_fn=make_deep_learning_model)

    model_without_params = model_map[model_name]
    model_with_params = model_without_params.set_params(**model_params)

    return model_with_params


def get_name_from_model(model):
    if isinstance(model, LogisticRegression):
        return 'LogisticRegression'
    if isinstance(model, RandomForestClassifier):
        return 'RandomForestClassifier'
    if isinstance(model, RidgeClassifier):
        return 'RidgeClassifier'
    if isinstance(model, GradientBoostingClassifier):
        return 'GradientBoostingClassifier'
    if isinstance(model, ExtraTreesClassifier):
        return 'ExtraTreesClassifier'
    if isinstance(model, AdaBoostClassifier):
        return 'AdaBoostClassifier'
    if isinstance(model, SGDClassifier):
        return 'SGDClassifier'
    if isinstance(model, Perceptron):
        return 'Perceptron'
    if isinstance(model, PassiveAggressiveClassifier):
        return 'PassiveAggressiveClassifier'
    if isinstance(model, LinearRegression):
        return 'LinearRegression'
    if isinstance(model, RandomForestRegressor):
        return 'RandomForestRegressor'
    if isinstance(model, Ridge):
        return 'Ridge'
    if isinstance(model, ExtraTreesRegressor):
        return 'ExtraTreesRegressor'
    if isinstance(model, AdaBoostRegressor):
        return 'AdaBoostRegressor'
    if isinstance(model, RANSACRegressor):
        return 'RANSACRegressor'
    if isinstance(model, GradientBoostingRegressor):
        return 'GradientBoostingRegressor'
    if isinstance(model, Lasso):
        return 'Lasso'
    if isinstance(model, ElasticNet):
        return 'ElasticNet'
    if isinstance(model, LassoLars):
        return 'LassoLars'
    if isinstance(model, OrthogonalMatchingPursuit):
        return 'OrthogonalMatchingPursuit'
    if isinstance(model, BayesianRidge):
        return 'BayesianRidge'
    if isinstance(model, ARDRegression):
        return 'ARDRegression'
    if isinstance(model, SGDRegressor):
        return 'SGDRegressor'
    if isinstance(model, PassiveAggressiveRegressor):
        return 'PassiveAggressiveRegressor'
    if isinstance(model, MiniBatchKMeans):
        return 'MiniBatchKMeans'

    if xgb_installed:
        if isinstance(model, xgb.XGBClassifier):
            return 'XGBClassifier'
        if isinstance(model, xgb.XGBRegressor):
            return 'XGBRegressor'

    if keras_installed:
        if isinstance(model, KerasRegressor):
            return 'DeepLearningRegressor'
        if isinstance(model, KerasClassifier):
            return 'DeepLearningClassifier'

    if lgb_installed:
        if isinstance(model, lgb.LGBMClassifier):
            return 'LGBMClassifier'
        if isinstance(model, lgb.LGBMRegressor):
            return 'LGBMRegressor'

# Hyperparameter search spaces for each model
def get_search_params(model_name):
    grid_search_params = {
        'DeepLearningRegressor': {
            'hidden_layers': [
                [1],
                [1, 0.1],
                [1, 1, 1],
                [1, 0.5, 0.1],
                [2],
                [5],
                [1, 0.5, 0.25, 0.1, 0.05],
                [1, 1, 1, 1],
                [1, 1]

                # [1],
                # [0.5],
                # [2],
                # [1, 1],
                # [0.5, 0.5],
                # [2, 2],
                # [1, 1, 1],
                # [1, 0.5, 0.5],
                # [0.5, 1, 1],
                # [1, 0.5, 0.25],
                # [1, 2, 1],
                # [1, 1, 1, 1],
                # [1, 0.66, 0.33, 0.1],
                # [1, 2, 2, 1]
            ]
            # , 'dropout_rate': [0.0, 0.2, 0.4, 0.6, 0.8]
            # # , 'weight_constraint': [0, 1, 3, 5]
            # , 'optimizer': ['SGD', 'RMSprop', 'Adagrad', 'Adadelta', 'Adam', 'Adamax', 'Nadam']
        },
        'DeepLearningClassifier': {
            'hidden_layers': [
                [1],
                [0.5],
                [2],
                [1, 1],
                [0.5, 0.5],
                [2, 2],
                [1, 1, 1],
                [1, 0.5, 0.5],
                [0.5, 1, 1],
                [1, 0.5, 0.25],
                [1, 2, 1],
                [1, 1, 1, 1],
                [1, 0.66, 0.33, 0.1],
                [1, 2, 2, 1]
            ]
            , 'optimizer': ['SGD', 'RMSprop', 'Adagrad', 'Adadelta', 'Adam', 'Adamax', 'Nadam']
            # , 'epochs': [2, 4, 6, 10, 20]
            # , 'batch_size': [10, 25, 50, 100, 200, 1000]
            # , 'lr': [0.001, 0.01, 0.1, 0.3]
            # , 'momentum': [0.0, 0.3, 0.6, 0.8, 0.9]
            # , 'init_mode': ['uniform', 'lecun_uniform', 'normal', 'zero', 'glorot_normal', 'glorot_uniform', 'he_normal', 'he_uniform']
            # , 'activation': ['softmax', 'softplus', 'softsign', 'relu', 'tanh', 'sigmoid', 'hard_sigmoid', 'linear']
            # , 'weight_constraint': [1, 3, 5]
            , 'dropout_rate': [0.0, 0.3, 0.6, 0.8, 0.9]
        },
        'XGBClassifier': {
            'max_depth': [1, 5, 10, 15],
            'learning_rate': [0.1],
            'min_child_weight': [1, 5, 10, 50],
            'subsample': [0.5, 0.8, 1.0],
            'colsample_bytree': [0.5, 0.8, 1.0]
            # 'subsample': [0.5, 1.0]
            # 'lambda': [0.9, 1.0]
        },
        'XGBRegressor': {
            # Add in max_delta_step if classes are extremely imbalanced
            'max_depth': [1, 3, 8, 25],
            # 'lossl': ['ls', 'lad', 'huber', 'quantile'],
            # 'booster': ['gbtree', 'gblinear', 'dart'],
            # 'objective': ['reg:linear', 'reg:gamma'],
            # 'learning_rate': [0.01, 0.1],
            'subsample': [0.5, 1.0]
            # 'subsample': [0.4, 0.5, 0.58, 0.63, 0.68, 0.76],

        },
        'GradientBoostingRegressor': {
            # Add in max_delta_step if classes are extremely imbalanced
            'max_depth': [1, 2, 3, 5],
            'max_features': ['sqrt', 'log2', None],
            # 'loss': ['ls', 'lad', 'huber', 'quantile']
            # 'booster': ['gbtree', 'gblinear', 'dart'],
            # 'loss': ['ls', 'lad', 'huber'],
            'loss': ['ls', 'huber'],
            # 'learning_rate': [0.01, 0.1, 0.25, 0.4, 0.7],
            'subsample': [0.5, 0.8, 1.0]
        },
        'GradientBoostingClassifier': {
            'loss': ['deviance', 'exponential'],
            'max_depth': [1, 2, 3, 5],
            'max_features': ['sqrt', 'log2', None],
            # 'learning_rate': [0.01, 0.1, 0.25, 0.4, 0.7],
            'subsample': [0.5, 1.0]
            # 'subsample': [0.4, 0.5, 0.58, 0.63, 0.68, 0.76]

        },

        'LogisticRegression': {
            'C': [.0001, .001, .01, .1, 1, 10, 100, 1000],
            'class_weight': [None, 'balanced'],
            'solver': ['newton-cg', 'lbfgs', 'sag']
        },
        'LinearRegression': {
            'fit_intercept': [True, False],
            'normalize': [True, False]
        },
        'RandomForestClassifier': {
            'criterion': ['entropy', 'gini'],
            'class_weight': [None, 'balanced'],
            'max_features': ['sqrt', 'log2', None],
            'min_samples_split': [1, 2, 5, 20, 50, 100],
            'min_samples_leaf': [1, 2, 5, 20, 50, 100],
            'bootstrap': [True, False]
        },
        'RandomForestRegressor': {
            'max_features': ['auto', 'sqrt', 'log2', None],
            'min_samples_split': [1, 2, 5, 20, 50, 100],
            'min_samples_leaf': [1, 2, 5, 20, 50, 100],
            'bootstrap': [True, False]
        },
        'RidgeClassifier': {
            'alpha': [.0001, .001, .01, .1, 1, 10, 100, 1000],
            'class_weight': [None, 'balanced'],
            'solver': ['auto', 'svd', 'cholesky', 'lsqr', 'sparse_cg', 'sag']
        },
        'Ridge': {
            'alpha': [.0001, .001, .01, .1, 1, 10, 100, 1000],
            'solver': ['auto', 'svd', 'cholesky', 'lsqr', 'sparse_cg', 'sag']
        },
        'ExtraTreesRegressor': {
            'max_features': ['auto', 'sqrt', 'log2', None],
            'min_samples_split': [1, 2, 5, 20, 50, 100],
            'min_samples_leaf': [1, 2, 5, 20, 50, 100],
            'bootstrap': [True, False]
        },
        'AdaBoostRegressor': {
            'base_estimator': [None, LinearRegression(n_jobs=-1)],
            'loss': ['linear','square','exponential']
        },
        'RANSACRegressor': {
            'min_samples': [None, .1, 100, 1000, 10000],
            'stop_probability': [0.99, 0.98, 0.95, 0.90]
        },
        'Lasso': {
            'selection': ['cyclic', 'random'],
            'tol': [.0000001, .000001, .00001, .0001, .001],
            'positive': [True, False]
        },

        'ElasticNet': {
            'l1_ratio': [0.1, 0.3, 0.5, 0.7, 0.9],
            'selection': ['cyclic', 'random'],
            'tol': [.0000001, .000001, .00001, .0001, .001],
            'positive': [True, False]
        },

        'LassoLars': {
            'positive': [True, False],
            'max_iter': [50, 100, 250, 500, 1000]
        },

        'OrthogonalMatchingPursuit': {
            'n_nonzero_coefs': [None, 3, 5, 10, 25, 50, 75, 100, 200, 500]
        },

        'BayesianRidge': {
            'tol': [.0000001, .000001, .00001, .0001, .001],
            'alpha_1': [.0000001, .000001, .00001, .0001, .001],
            'lambda_1': [.0000001, .000001, .00001, .0001, .001],
            'lambda_2': [.0000001, .000001, .00001, .0001, .001]
        },

        'ARDRegression': {
            'tol': [.0000001, .000001, .00001, .0001, .001],
            'alpha_1': [.0000001, .000001, .00001, .0001, .001],
            'alpha_2': [.0000001, .000001, .00001, .0001, .001],
            'lambda_1': [.0000001, .000001, .00001, .0001, .001],
            'lambda_2': [.0000001, .000001, .00001, .0001, .001],
            'threshold_lambda': [100, 1000, 10000, 100000, 1000000]
        },

        'SGDRegressor': {
            'loss': ['squared_loss', 'huber', 'epsilon_insensitive', 'squared_epsilon_insensitive'],
            'penalty': ['none', 'l2', 'l1', 'elasticnet'],
            'learning_rate': ['constant', 'optimal', 'invscaling'],
            'alpha': [.0000001, .000001, .00001, .0001, .001]
        },

        'PassiveAggressiveRegressor': {
            'epsilon': [0.01, 0.05, 0.1, 0.2, 0.5],
            'loss': ['epsilon_insensitive', 'squared_epsilon_insensitive'],
            'C': [.0001, .001, .01, .1, 1, 10, 100, 1000],
        },

        'SGDClassifier': {
            'loss': ['hinge', 'log', 'modified_huber', 'squared_hinge', 'perceptron', 'squared_loss', 'huber', 'epsilon_insensitive', 'squared_epsilon_insensitive'],
            'penalty': ['none', 'l2', 'l1', 'elasticnet'],
            'alpha': [.0000001, .000001, .00001, .0001, .001],
            'learning_rate': ['constant', 'optimal', 'invscaling'],
            'class_weight': ['balanced', None]
        },

        'Perceptron': {
            'penalty': ['none', 'l2', 'l1', 'elasticnet'],
            'alpha': [.0000001, .000001, .00001, .0001, .001],
            'class_weight': ['balanced', None]
        },

        'PassiveAggressiveClassifier': {
            'loss': ['hinge', 'squared_hinge'],
            'class_weight': ['balanced', None],
            'C': [0.01, 0.3, 0.5, 0.7, 0.8, 0.9, 0.95, 0.99, 1.0]
        }

        , 'LGBMClassifier': {
            # 'max_bin': [25, 50, 100, 200, 250, 300, 400, 500, 750, 1000]
            'num_leaves': [10, 20, 30, 40, 50, 200]
            , 'colsample_bytree': [0.7, 0.9, 1.0]
            , 'subsample': [0.7, 0.9, 1.0]
            # , 'subsample_freq': [0.3, 0.5, 0.7, 0.9, 1.0]
            , 'learning_rate': [0.01, 0.05, 0.1]
            # , 'subsample_for_bin': [1000, 10000]
            , 'n_estimators': [5, 20, 50, 200]

        }

        , 'LGBMRegressor': {
            # 'max_bin': [25, 50, 100, 200, 250, 300, 400, 500, 750, 1000]
            'num_leaves': [10, 20, 30, 40, 50, 200]
            , 'colsample_bytree': [0.7, 0.9, 1.0]
            , 'subsample': [0.7, 0.9, 1.0]
            # , 'subsample_freq': [0.3, 0.5, 0.7, 0.9, 1.0]
            , 'learning_rate': [0.01, 0.05, 0.1]
            # , 'subsample_for_bin': [1000, 10000]
            , 'n_estimators': [5, 20, 50, 200]

        }

    }

    # Some of these are super expensive to compute. So if we're running this in a test suite, let's make sure the structure works, but reduce the compute time
    params = grid_search_params[model_name]
    if 'is_test_suite' in sys.argv:
        simplified_params = {}
        for k, v in params.items():
            # Grab the first two items for each thing we want to test
            simplified_params[k] = v[:2]
        params = simplified_params

    return params


def load_keras_model(file_name):
    from keras.models import load_model

    with open(file_name, 'rb') as read_file:
        base_pipeline = dill.load(read_file)

    keras_file_name = file_name[:-5] + '_keras_deep_learning_model.h5'

    keras_model = load_model(keras_file_name)

    base_pipeline.named_steps['final_model'].model = keras_model

    return base_pipeline


def make_deep_learning_model(hidden_layers=None, num_cols=None, optimizer='adam', dropout_rate=0.2, weight_constraint=0):
    if hidden_layers is None:
        hidden_layers = [1, 1, 1]

    # The hidden_layers passed to us is simply describing a shape. it does not know the num_cols we are dealing with, it is simply values of 0.5, 1, and 2, which need to be multiplied by the num_cols
    scaled_layers = []
    for layer in hidden_layers:
        scaled_layers.append(int(num_cols * layer))


    model = Sequential()

    model.add(Dense(hidden_layers[0], input_dim=num_cols, init='normal', activation='relu'))

    for layer_size in scaled_layers[1:]:
        model.add(Dense(layer_size, init='normal', activation='relu'))
    # For regressors, we want an output layer with a single node
    model.add(Dense(1, init='normal'))

    # The final step is to compile the model
    model.compile(loss='mean_squared_error', optimizer=optimizer, metrics=['mean_absolute_error', 'mean_absolute_percentage_error'])

    return model


def make_deep_learning_classifier(hidden_layers=None, num_cols=None, optimizer='adam', dropout_rate=0.2, weight_constraint=0, final_activation='sigmoid'):

    if hidden_layers is None:
        hidden_layers = [1, 1, 1]

    # The hidden_layers passed to us is simply describing a shape. it does not know the num_cols we are dealing with, it is simply values of 0.5, 1, and 2, which need to be multiplied by the num_cols
    scaled_layers = []
    for layer in hidden_layers:
        scaled_layers.append(int(num_cols * layer))


    model = Sequential()

    model.add(Dense(hidden_layers[0], input_dim=num_cols, init='normal', activation='relu'))

    for layer_size in scaled_layers[1:]:
        model.add(Dense(layer_size, init='normal', activation='relu'))

    model.add(Dense(1, init='normal', activation=final_activation))
    model.compile(loss='binary_crossentropy', optimizer=optimizer, metrics=['accuracy', 'poisson'])
    return model
