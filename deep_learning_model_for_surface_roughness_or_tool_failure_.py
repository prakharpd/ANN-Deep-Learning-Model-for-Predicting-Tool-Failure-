# -*- coding: utf-8 -*-
"""Deep Learning Model For Surface Roughness or Tool Failure .ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1fwhyO8fPwu3lL07QUZwdtgLZCEjCN42O

# Deep Learning Model
# All copyrights belongs to © Prakhar Dwivedi
### Importing the libraries
"""

import numpy as np
import pandas as pd
import tensorflow as tf

tf.__version__

"""## Part 1 - Data Preprocessing

### Importing the dataset
"""

dataset = pd.read_csv('Parameter.csv')
X = dataset.iloc[:, 3:-1].values
y = dataset.iloc[:, -1].values

print(X)

print(y)

"""### Encoding categorical data

Label Encoding the "ToolUsed" column
"""

from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
X[:, 2] = le.fit_transform(X[:, 2])

print(X)   # 1 -> Turning
           # 0 -> Knurling

"""One Hot Encoding the "Geography" column"""

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), [1])], remainder='passthrough')
X = np.array(ct.fit_transform(X))

print(X)

"""### Splitting the dataset into the Training set and Test set"""

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

"""### Feature Scaling"""

from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

"""## Part 2 - Building the ANN - Core Component of Deep Learning

### Initializing the ANN
"""

ann = tf.keras.models.Sequential()   # Making 'ann' variable into a object created from the instances of sequential class.

"""### Adding the input layer and the first hidden layer"""

ann.add(tf.keras.layers.Dense(units=6, activation= 'relu'))   # From 'ann' we are creating dancing class.

# units in Dense() class creates number of hidden layers of neurons into it.
# Activation function in hidden layers should be Rectifier Activation Function. i.e. 'relu'

"""### Adding the second hidden layer"""

ann.add(tf.keras.layers.Dense(units=6, activation= 'relu'))

"""### Adding the output layer"""

ann.add(tf.keras.layers.Dense(units=1, activation= 'sigmoid'))    # This is output code. Since our output data is Binary hence 'units =1'

# If it was Classification Model (having multiple options as result we will use 'units =3' that too after one-hot encoding those outputs).

# In Output layer our 'activation function' would be 'sigmoid' because it gives result as well as probability.

"""## Part 3 - Training the ANN

### Compiling the ANN
"""

ann.compile(optimizer = 'adam' , loss ='binary_crossentropy' , metrics = ['accuracy'])

"""### Training the ANN on the Training set"""

ann.fit(X_train, y_train, batch_size = 32, epochs = 100)  # We are doing batch learning. epoch is learning strength

"""## Part 4 - Making the predictions and evaluating the model

### Predicting the result of a single observation

Using our Deep Learning Model to predict if the tool with the following informations will undergo tool failure in operation:

Geography: France

Performance Score: 600

Tool Used: Turning

Rated Tool Life on Daily Use: 40 months

Expected Tenure(in years): 3 years

Frequency Of Use: 60000

Number of Products (In Hundred Thousand): 2

Wheteher lubricants are used while operation ? Yes

Is Actively Used ?: Yes

Estimated Unit Cost: $ 50000

So, should we say goodbye to that tool ?

**Approach**

Therefore, our ANN model predicts that this customer stays in the bank!

**Important note 1:** Notice that the values of the features were all input in a double pair of square brackets. That's because the "predict" method always expects a 2D array as the format of its inputs. And putting our values into a double pair of square brackets makes the input exactly a 2D array.

**Important note 2:** Notice also that the "France" country was not input as a string in the last column but as "1, 0, 0" in the first three columns. That's because of course the predict method expects the one-hot-encoded values of the state, and as we see in the first row of the matrix of features X, "France" was encoded as "1, 0, 0". And be careful to include these values in the first three columns, because the dummy variables are always created in the first columns.
"""

print(ann.predict(sc.transform([[1, 0, 0, 600, 1, 40, 3, 60000 , 2 , 1 , 1 , 50000]])))    # Anything we need to predict need to be 2D Array. Hence we need to add double pair of brackets.
# Adittionally, in ANN we need to scale that data set for predicting particular Row.

# To get final answer in True or False.

print(ann.predict(sc.transform([[1, 0, 0, 600, 1, 40, 3, 60000 , 2 , 1 , 1 , 50000]])) > 0.5)

"""### Predicting the Test set results"""

y_pred = ann.predict(X_test)
y_pred = (y_pred > 0.5)
print(np.concatenate((y_pred.reshape(len(y_pred),1), y_test.reshape(len(y_test),1)),1))

"""### Making the Confusion Matrix"""

from sklearn.metrics import confusion_matrix, accuracy_score
cm = confusion_matrix(y_test, y_pred)
print(cm)
accuracy_score(y_test, y_pred)
