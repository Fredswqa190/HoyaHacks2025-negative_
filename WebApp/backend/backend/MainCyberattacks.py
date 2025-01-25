import tensorflow as tf
import sqlite3
import pandas as pd
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix, precision_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler, MultiLabelBinarizer
from keras.models import Sequential
from keras.layers import Dense, LSTM
from keras.utils import to_categorical
import re
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, confusion_matrix
conn1 = sqlite3.connect('EU-Cyberattacks.db')
conn2 = sqlite3.connect('Global-Cyberattacks.db')
conn3 = sqlite3.connect('EU-Cyberwarfareattacks.db')
conn4 = sqlite3.connect('Global-Cyberwarfareattacks.db')  #import all databases into the system
cursor1 = conn1.execute("SELECT AttackType,AttackIntensity,AttackTarget,AttackCountry,AttackAttribution FROM CyberAttacks") #SELECT query via SQL to select
data1 = cursor1.fetchall()
cursor2 = conn2.execute("SELECT AttackType,AttackIntensity,AttackTarget,AttackCountry,AttackAttribution FROM CyberAttacks")
data2 = cursor2.fetchall()
cursor3 = conn3.execute("SELECT AttackType,AttackIntensity,AttackTarget,AttackCountry,AttackAttribution FROM CyberwarfareAttacks")
data3 = cursor3.fetchall()
cursor4 = conn4.execute("SELECT AttackType,AttackIntensity,AttackTarget,AttackCountry,AttackAttribution FROM CyberwarfareAttacks")
data4 = cursor4.fetchall()
#print(data4)
#create pandas dataframe
df1 = pd.DataFrame(data1, columns=['AttackType', 'AttackIntensity', 'AttackTarget', 'AttackCountry', 'AttackAttribution'])
df2 = pd.DataFrame(data2, columns=['AttackType', 'AttackIntensity', 'AttackTarget', 'AttackCountry', 'AttackAttribution']) #Attack ID, Attack Desc, Attack Date, Attack Country, Attack Country, Attack Target, Attack Method, Attack Attribution
combined_data1_2 = pd.concat([df1, df2], axis=0, ignore_index=True)
combined_data1_2.to_csv('combined_data1_2.csv', index=False)
df3 = pd.DataFrame(data3, columns=['AttackType', 'AttackIntensity', 'AttackTarget', 'AttackCountry', 'AttackAttribution'])
df4 = pd.DataFrame(data4, columns=['AttackType', 'AttackIntensity', 'AttackTarget', 'AttackCountry', 'AttackAttribution'])
combined_data3_4 = pd.concat([df3, df4], axis=0, ignore_index=True)
combined_data3_4.to_csv('combined_data3_4.csv', index=False)
#This code is assigning dataframe 1 and 2 to data1 and data2 respectively then combines them, same applies to df3 and df4.
#print(df2)
#df = pd.concat([df1, df2], axis=0)
#These two dataframes will segregate cyber attacks and cyberwarfare attacks
cyber_attacks = combined_data1_2[combined_data1_2['AttackType'] == 'cyber_attack']
cyber_warfare_attacks = combined_data3_4[combined_data3_4['AttackType'] == 'cyber_warfare_attack']
#print(cyber_attacks)
# Load combined_data1_2.csv
df1 = pd.read_csv('combined_data1_2.csv')
# Load combined_data3_4.csv
df2 = pd.read_csv('combined_data3_4.csv')
df = pd.concat([df1, df2], axis=0, ignore_index=True)
# Preprocess data
df.loc[df['AttackType'].str.contains('Cyberwarfare_attack'), 'AttackType'] = 'Cyberwarfare'
df.loc[df['AttackType'].str.contains('cyber_attack'), 'AttackType'] = 'Cyber Attack'
le = LabelEncoder()
df['AttackType'] = le.fit_transform(df['AttackType'])
# transform the 'AttackAttribution' column
#df['AttackAttribution'] = le.fit_transform(df['AttackAttribution'])
# print the unique values in the 'AttackAttribution' column
#print(df['AttackAttribution'].unique())
df['AttackIntensity'] = le.fit_transform(df['AttackIntensity'])
df['AttackTarget'] = le.fit_transform(df['AttackTarget'])
df['AttackCountry'] = le.fit_transform(df['AttackCountry'])
df_filtered1 = df[(df['AttackAttribution'].str.contains('Attack conducted by nation state (generic state-attribution or direct attribution towards specific state-entities, e.g., intelligence agencies); Attack on (inter alia) political target(s), politicized')) |
                 (df['AttackAttribution'].str.contains('Attack conducted by nation state (generic state-attribution or direct attribution towards specific state-entities, e.g., intelligence agencies); Attack on (inter alia) political target(s), not politicized', na=False)) |
                 (df['AttackAttribution'].str.contains('Attack conducted by non-state group / non-state actor with political goals (religious, ethnic, etc. groups) / undefined actor with political goals; Attack on (inter alia) political target(s), not politicized', na=False)) |
                 (df['AttackAttribution'].str.contains('Attack conducted by nation state (generic state-attribution or direct attribution towards specific state-entities, e.g., intelligence agencies)', na=False)) |
                 (df['AttackAttribution'].str.contains('Attack conducted by non-state group / non-state actor with political goals (religious, ethnic, etc. groups) / undefined actor with political goals; Attack on (inter alia) political target(s), politicized', na=False)) |
                 (df['AttackAttribution'].str.contains('Attack conducted by non-state group / non-state actor with political goals (religious, ethnic, etc. groups) / undefined actor with political goals; Attack on non-political target(s), politicized', na=False)) |
                 (df['AttackAttribution'].str.contains('Attack on (inter alia) political target(s), not politicized', na=False)) |
                 (df['AttackAttribution'].str.contains('Attack on (inter alia) political target(s), not politicized; Attack on (inter alia) political target(s), not politicized', na=False)) |
                 (df['AttackAttribution'].str.contains('Attack on (inter alia) political target(s), not politicized; Attack on (inter alia) political target(s), politicized', na=False)) |
                 (df['AttackAttribution'].str.contains('Attack on (inter alia) political target(s), politicized', na=False)) |
                 (df['AttackAttribution'].str.contains('Attack on non-political target(s), politicized', na=False))]
#print(df_filtered1.columns)
#choicelist = [
    #df['AttackAttribution'] == 'Attack conducted by nation state (generic state-attribution or direct attribution towards specific state-entities, e.g., intelligence agencies); Attack on (inter alia) political target(s), politicized' ,
    #df['AttackAttribution'] == 'Attack conducted by nation state (generic state-attribution or direct attribution towards specific state-entities, e.g., intelligence agencies); Attack on (inter alia) political target(s), not politicized' ,
    #df['AttackAttribution'] == 'Attack conducted by non-state group / non-state actor with political goals (religious, ethnic, etc. groups) / undefined actor with political goals; Attack on (inter alia) political target(s), not politicized' ,
    #df['AttackAttribution'] == 'Attack conducted by nation state (generic state-attribution or direct attribution towards specific state-entities, e.g., intelligence agencies)' ,
    #df['AttackAttribution'] == 'Attack conducted by non-state group / non-state actor with political goals (religious, ethnic, etc. groups) / undefined actor with political goals; Attack on (inter alia) political target(s), politicized' ,
    #df['AttackAttribution'] == 'Attack conducted by non-state group / non-state actor with political goals (religious, ethnic, etc. groups) / undefined actor with political goals; Attack on non-political target(s), politicized' ,
    #df['AttackAttribution'] == 'Attack on (inter alia) political target(s), not politicized' ,
    #df['AttackAttribution'] == 'Attack on (inter alia) political target(s), not politicized; Attack on (inter alia) political target(s), not politicized' ,
    #df['AttackAttribution'] == 'Attack on (inter alia) political target(s), not politicized; Attack on (inter alia) political target(s), politicized' ,
    #df['AttackAttribution'] == 'Attack on (inter alia) political target(s), politicized' ,
    #df['AttackAttribution'] == 'Attack on non-political target(s), politicized' ,
#]
# define a function to split the string by the delimiter on a per-row basis
def split_row(row):
    # check if the delimiter is present in the row
    if ";" in row["AttackAttribution"]:
        # split the string by the delimiter and return as a list
        return row["AttackAttribution"].split(";")
    else:
        # if delimiter is not present, return an empty list
        return [row['AttackAttribution']]

# apply the split_row function to each row in the dataframe
attribution_lists = df.apply(split_row, axis=1).tolist()
# remove empty lists from attribution_lists
attribution_lists = [x for x in attribution_lists if x]

# fit and transform the multilabelbinarizer on the lists of substrings
mlb = MultiLabelBinarizer()
attribution_encoded = mlb.fit_transform(attribution_lists)

#print(attribution_lists)
# concatenate the numpy array labels with the transformed attribution
labels = df['AttackType'].to_numpy()

#debugging
#print(attribution_encoded.shape)
#print(labels.shape)
#print(attribution_encoded.dtype)
#print(labels.dtype)
#print("Encoded attribution:\n", attribution_encoded)
#print("Original AttackAttribution:\n", df['AttackAttribution'])
data = np.concatenate((attribution_encoded, labels.reshape(-1, 1)), axis=1)

# Use MultiLabelBinarizer to binarize the AttackAttribution column
attack_attributions = mlb.fit_transform(df['AttackAttribution'])

# Define the model
model = Sequential()
model.add(Dense(32, input_shape=(2,), activation='relu'))
model.add(Dense(16, activation='relu'))
model.add(Dense(8, activation='relu'))
model.add(Dense(2, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='sgd', metrics=['accuracy'])

# print the model summary
model.summary()

#X_train = df.drop(['AttackType'], axis=1)
#y_train = df['AttackType'].values
#X_test = df.drop(['AttackType'], axis=1).values
# convert y_train to numpy array and reshape it
# Split data into training and test sets
#X_train, X_test, y_train, y_test = train_test_split(df_filtered1.drop(['AttackType'], axis=1), y_encoded, test_size=0.2)
y_test = df['AttackType'].values
X = df.drop(['AttackType', 'AttackCountry'], axis=1).values
y = mlb.fit_transform(df['AttackType'].values.reshape(-1, 1))

# encode the target variable before splitting the data
y_encoded = mlb.fit_transform(df['AttackType'].apply(lambda x: [x]))
# get list of encoded labels in test set
#y_test_list = y_test.tolist()
#y_test_array = np.array(y_test_list).reshape(1, -1)
#y_test = np.array(y_test)

# Split data into training and test sets
X_train, X_test, y_train_encoded, y_test_encoded = train_test_split(df.drop(['AttackType', 'AttackCountry'], axis=1), y_encoded, test_size=0.2, random_state=42)


# convert encoded labels to list and reshape
y_train = mlb.inverse_transform(y_train_encoded)
y_test = mlb.inverse_transform(y_test_encoded)
# Split data into training and test sets
#X_train, X_test, y_train_encoded, y_test_encoded = train_test_split(df.drop(['AttackType'], axis=1), y_encoded, test_size=0.2, random_state=42)
# get list of classes in the trained model
mlb_classes_list = mlb.classes_.tolist()

# convert to numpy array and reshape it
mlb_classes_array = np.array(mlb_classes_list).reshape(-1, 1)

# transform the classes array
mlb_classes_encoded = mlb.transform(mlb_classes_array)
# find any unseen categories in the test set
unseen_categories = set(tuple(label) for label in y_test_encoded) - set(tuple(label) for label in mlb_classes_encoded)
if unseen_categories:
    print(f"Found unseen categories: {unseen_categories}")

    # remove any unseen categories from the test set
    mask = np.array([tuple(label) not in unseen_categories for label in y_test_encoded])
    y_test_encoded = y_test_encoded[mask]

    # convert back to list format
    y_test_encoded_list = [list(label) for label in y_test_encoded]

    # update test set
    y_test = mlb.inverse_transform(y_test_encoded)
#print(X_train)
#print(y_train_encoded)
# convert numpy array to pandas dataframe
X_train_df = pd.DataFrame(X_train)

# select only numeric columns
#X_train = df.values.reshape((df.shape[0], df.shape[1]))
X_train = X_train_df.select_dtypes(include=['int64', 'float64', 'float32'])
X_train = X_train.values
#X_test = df.values.reshape((df.shape[0], df.shape[1]))
X_test= X_test.select_dtypes(include=['int64', 'float64', 'float32'])
X_test = X_test.values
#print(X_train)
#print(y_train_encoded)
# Train and evaluate your model
#print("Shape of X_train_numeric:", X_train_numeric.shape)
#print("Shape of y_train_encoded:", y_train_encoded.shape)
#print(X_train.shape)
#print(model.input_shape)
#print(y_test_encoded)
#print(X_test.dtype)
#print(y_test_encoded.dtype)
# create boolean mask of rows in X_test corresponding to y_test_encoded
#mask = np.array([tuple(img) in y_test_encoded for img in X_test])
# Use the new boolean mask to index the X_test and y_test_encoded arrays
#X_test = X_test[mask]
#y_test_encoded = y_test_encoded[mask]
# Check the dimensions of the new X_test and y_test_encoded arrays
#print(X_test.shape)        # should be (63, 2)
#print(y_test_encoded.shape) # should be (63, ...)
#mask = mask.reshape(-1, 1)  # Reshape mask to have a second dimension of 1
# select corresponding rows in y_test_encoded
#y_test_encoded = y_test_encoded[mask]
# Check the dimensions of your boolean mask and your array
#print(len(mask))
#print(len(y_test_encoded))
# select corresponding rows in X_test
#X_test = X_test[mask]
#print(y_train_encoded.shape)
# Fit the model
#print(y_train_encoded.dtype)
model.fit(X_train, y_train_encoded, epochs=50, validation_data=(X_test, y_test_encoded))
# convert y_test_encoded to a tensor
#print(X_test)
#print(y_test_encoded.dtype)
# evaluate model on test set
test_loss, test_acc = model.evaluate(X_test, y_test_encoded)
print('Test loss:', test_loss)
print('Test accuracy:', test_acc)
# calculate precision
y_pred_encoded = model.predict(X_test)
precision = precision_score(y_test_encoded, y_pred_encoded.round(), average='micro')
#test precision measurement 
print('Precision:', precision)

##F1 score implementation
# Predict on the test set
#y_pred_encoded = model.predict(X_test)
#y_pred = mlb.inverse_transform(y_pred_encoded)

# Calculate the F1 score
#f1 = f1_score(y_test, y_pred, average='micro')
#print('F1 score:', f1)