Example of using the generalized_blender module to run classification ensembles




"""
Trains a series of base models using K-fold cross-validation, then combines
the predictions of each model into a set of features that are used to train
a high-level set of blending models model.

Currently only classification models are supported

Parameters
-----------
base_models:
    A list of models to be run as part of base learners on original
    training dataset
Each model must have a .fit and .predict_proba/.predict method a'la
sklearn
blending_models:
A list of models used to aggregate the outputs of the trained base
models. Must have a .fit and .predict_proba/.predict method
n_folds: int
The number of K-folds to use in =cross-validated model training.
    Currently upto 7 folds are supported
verbose: boolean
nclasses: Mention the number of classes in target variable

batch: batch size to be used for Keras models
base_epochs: no of epochs to be used for Keras in base_models
second_epochs: no of epochs to be used for Keras in blending_models

Example
-------
# First define the list of base models and blending models you intend to use.
    # For models other than Xgboost and Keras neural networks the user can define
      model parameters within the base_models and blending_models lists.

base_models = ['xgb1', LogisticRegression(C=0.1), 'xgb2', 'keras1']
blending_models = ['keras1','keras2','xgb1']
verbose = True
nclasses = len(targetencoder.classes_)
n_folds =2


# Depending on number of XGBoost models defined in base_models and blending_models
  define XGBoost parameters. Here, we're using 2 XGBoost models in base_models and
  1 XGBoost model in blending_models.

  After defining parameters, put all base_models XGBOost parameters in a list and
  do the same for blending_models XGBoost parameters

# params1
eta1 = 0.02
max_depth1 = 20
subsample1 = 0.6
colsample_bytree1 = 0.7
random_state1 = 10
num_boost_round1 = 50
early_stopping_rounds1 = 3
print('XGBoost params. ETA: {}, MAX_DEPTH: {}, SUBSAMPLE: {}, COLSAMPLE_BY_TREE: {}'.format(eta1, max_depth1, subsample1, colsample_bytree1))
params1 = {
        "objective": "multi:softprob",
        "num_class": 12,
        "booster" : "gblinear",
        "eval_metric": "mlogloss",
        "eta": eta1,
        "max_depth": max_depth1,
        "subsample": subsample1,
        "colsample_bytree": colsample_bytree1,
        "silent": 1,
        "seed": random_state1,
        "num_boost_round": num_boost_round1,
        "early_stopping_rounds": early_stopping_rounds1

}

# params2
eta2 = 0.001
max_depth2 = 10
subsample2 = 0.75
colsample_bytree2 = 0.65
random_state2 = 11
num_boost_round2 = 35
early_stopping_rounds2 = 3

print('XGBoost params. ETA: {}, MAX_DEPTH: {}, SUBSAMPLE: {}, COLSAMPLE_BY_TREE: {}'.format(eta2, max_depth2, subsample2, colsample_bytree2))
params2 = {
        "objective": "multi:softprob",
        "num_class": 12,
        "booster" : "gblinear",
        "eval_metric": "mlogloss",
        "eta": eta2,
        "max_depth": max_depth2,
        "subsample": subsample2,
        "colsample_bytree": colsample_bytree2,
        "silent": 1,
        "seed": random_state2,
        "num_boost_round": num_boost_round2,
        "early_stopping_rounds": early_stopping_rounds2
}


xgb_parameters1 = [params1,params2]

# Second level XGBoost learner parameters

eta3 = 0.03
max_depth3 = 15
subsample3 = 0.6
colsample_bytree3 = 0.7
random_state3 = 203
num_boost_round3 = 5000
early_stopping_rounds3 = 1
print('XGBoost params. ETA: {}, MAX_DEPTH: {}, SUBSAMPLE: {}, COLSAMPLE_BY_TREE: {}'.format(eta3, max_depth3, subsample3, colsample_bytree3))
params3 = {
        "objective": "multi:softprob",
        "num_class": 12,
        "booster" : "gblinear",
        "eval_metric": "mlogloss",
        "eta": eta3,
        "max_depth": max_depth3,
        "subsample": subsample3,
        "colsample_bytree": colsample_bytree3,
        "silent": 1,
        "seed": random_state3,
        "num_boost_round": num_boost_round3,
        "early_stopping_rounds": early_stopping_rounds3

}


xgb_parameters2 = [params3]




# KERAS
    If Keras neural network models are being used in base_models and/or blending_models
    the user has to define some parameters and model structure for all Keras models being
    used

    Here 1 Keras model is used in base_models and 2 in blending_models

    First we define batch size for the Keras model to use. It is receommended that this
    number be divisible by the number of rows in training set

    Another point to note is that, if the input training set is in the form of a sparse
    matrix the Keras model uses a batch generator which to simulatneously sample the training
    dataset and build models and combine them

#
  batch = 400 # define batch size as a number that can divide the number of rows in training set

 # Next define the number of epochs i.e., number of times to go through the entire dataset
   The lists below should reflect the number of Keras defined under base_models and blending_models lists earlier
  base_epochs = [2] # number of times to go through the entire dataset in base_models level
  second_epochs = [2,2] # number of times to go through the entire dataset in blending_models level


 # Keras Structure for base models
def baseline_keras_model_1():
    # create model
    model = Sequential()
    model.add(Dense(250, input_dim=Xtrain.shape[1], init='normal'))
    model.add(PReLU())
    model.add(Dropout(0.4))
    model.add(Dense(60, init='normal'))
    model.add(PReLU())
    model.add(Dropout(0.2))
    model.add(Dense(12, init='normal', activation='softmax'))
    # Compile model
    model.compile(loss='sparse_categorical_crossentropy', optimizer='adadelta', metrics=['accuracy'])  #logloss
    return model

keras_basemodel_1 = baseline_keras_model_1()

keras_base_models = [keras_basemodel_1]


# Keras Structure for blending_models models

def secondlevel_keras_model_1():
    # create model
    model = Sequential()
    model.add(Dense(150, input_dim = len(base_models)*nclasses, init='normal'))
    model.add(PReLU())
    model.add(Dropout(0.4))
    model.add(Dense(50, init='normal'))
    model.add(PReLU())
    model.add(Dropout(0.2))
    model.add(Dense(12, init='normal', activation='softmax'))
    # Compile model
    model.compile(loss='sparse_categorical_crossentropy', optimizer='adadelta', metrics=['accuracy'])
    return model

keras_secondlevel_model_1 = secondlevel_keras_model_1()

def secondlevel_keras_model_2():
    # create model
    model = Sequential()
    model.add(Dense(50, input_dim = len(base_models)*nclasses, init='normal'))
    model.add(PReLU())
    model.add(Dropout(0.1))
    model.add(Dense(10, init='normal'))
    model.add(PReLU())
    model.add(Dropout(0.05))
    model.add(Dense(12, init='normal', activation='softmax'))
    # Compile model
    model.compile(loss='sparse_categorical_crossentropy', optimizer='adadelta', metrics=['accuracy'])
    return model

keras_secondlevel_model_2 = secondlevel_keras_model_2()

keras_secondlevel_models = [keras_secondlevel_model_1,keras_secondlevel_model_2]



######################################
######################################
Once the definition of parameters and other model related structures are done the user
can install and import the module from PyPi and user

# use pip install generalized_blender to install the latest version from PyPi

#Then use the following,

from generalized_blender import generalized_blender

# initialize the class object
blend_object = generalized_blender.Blender(base_models, blending_models,n_folds,True,nclasses)

# Running base models
A, B = blend_object.base_learners(Xtrain,Xtest,y,xgb_parameters1, base_epochs,batch,keras_base_models)

The above function returns predictions from the base_level models on both training and test
datasets which serve as inputs to the blending models next

# Running Blending models
Result = blend_object.blender(A,B,y,xgb_parameters2, second_epochs, batch, keras_secondlevel_models)

The 'Result' dataset is basically a numpy array of all predicted probabilities for each classfor all
blending_models. For instance, here the number of blending_models is 3 and number of target
variable classes is 12. So the 'Result' array will have 36 columns

# The user can then take the 'Result' and compute either mean, geo mean or other metric
to combine all blending_models predictions or even feed them into another level of modeling





"""
