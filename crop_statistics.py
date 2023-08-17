import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

from ipywidgets import interact


data = pd.read_csv("/content/data.csv")
print(data)

sns.heatmap(data.isnull())

#### Seasonal Crop
# Summer crop
print(data[ (data['temperature'] > 30) & (data['humidity'] > 50) ]['label'].unique())
# Winter crop
print(data[ (data['temperature'] < 20) & (data['humidity'] > 30) ]['label'].unique())
# Monsoon crop
print(data[ (data['rainfall'] > 200) & (data['humidity'] > 30) ]['label'].unique())


plt.subplot(3, 4, 1)
sns.histplot(data['N'], color='blue')
plt.xlabel('N')
plt.grid()

plt.subplot(3, 4, 2)
sns.histplot(data['P'], color='yellow')
plt.xlabel('P')
plt.grid()

plt.subplot(3, 4, 3)
sns.histplot(data['K'], color='red')
plt.xlabel('K')
plt.grid()

plt.subplot(3, 4, 4)
sns.histplot(data['temperature'], color='grey')
plt.xlabel('temperature')
plt.grid()

plt.subplot(2, 4, 5)
sns.histplot(data['humidity'], color='green')
plt.xlabel('humidity')
plt.grid()

plt.subplot(2, 4, 6)
sns.histplot(data['ph'], color='blue')
plt.xlabel('ph')
plt.grid()

plt.subplot(2, 4, 7)
sns.histplot(data['rainfall'], color='red')
plt.xlabel('rainfall')
plt.grid()

@interact
def summary(crops=list(data['label'].value_counts().index)):
  x = data[data['label'] == crops]
  print("Maximum N required: ", x['N'].max())
  print("Minimum N required: ", x['N'].min())
  print("Average N required: ", x['N'].mean())

  print("-----------------------------------")
  
  print("Maximum N required: ", x['P'].max())
  print("Minimum N required: ", x['P'].min())
  print("Average N required: ", x['P'].mean())

  print("-----------------------------------")

  print("Maximum N required: ", x['K'].max())
  print("Minimum N required: ", x['K'].min())
  print("Average N required: ", x['K'].mean())

  print("-----------------------------------")

  print("Maximum N required: ", x['temperature'].max())
  print("Minimum N required: ", x['temperature'].min())
  print("Average N required: ", x['temperature'].mean())

  print("-----------------------------------")

  print("Maximum N required: ", x['humidity'].max())
  print("Minimum N required: ", x['humidity'].min())
  print("Average N required: ", x['humidity'].mean())

  print("-----------------------------------")

  print("Maximum N required: ", x['ph'].max())
  print("Minimum N required: ", x['ph'].min())
  print("Average N required: ", x['ph'].mean())

  print("-----------------------------------")
  
  print("Maximum N required: ", x['rainfall'].max())
  print("Minimum N required: ", x['rainfall'].min())
  print("Average N required: ", x['rainfall'].mean())


# elbow method
from pandas.core.common import random_state
from sklearn.cluster import KMeans 

x = data.drop(['label'], axis=1).values
y = data['label']
wcss = []

for i in range(1, 11):
  km = KMeans(n_clusters=i, init="k-means++", max_iter=2000, random_state=0)
  km.fit(x)
  wcss.append(km.inertia_)

plt.plot(range(1, 11), wcss)


km = KMeans(n_clusters=4, init="k-means++", max_iter=2000, random_state=0)
y_means = km.fit_predict(x)
a = data['label']
y_means = pd.DataFrame(y_means)
z = pd.concat([y_means, a], axis=1)
z = z.rename(columns={0:"cluster"})

print("Cluster 0", z[z["cluster"]==0]["label"].unique())


print("Cluster 1", z[z["cluster"]==1]["label"].unique())

print("Cluster 2", z[z["cluster"]==2]["label"].unique())

print("Cluster 4", z[z["cluster"]==3]["label"].unique())

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=.2, random_state=42)


from sklearn.linear_model import LogisticRegression
model = LogisticRegression()
model.fit(x_train, y_train)

y_pred = model.predict(x_test)

from sklearn.metrics import classification_report
cr = classification_report(y_test, y_pred)
print(cr)

from sklearn.metrics import confusion_matrix
plt.rcParams['figure.figsize'] = (10, 10)
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True)

pred = model.predict([[50, 50, 30, 36, 60, 7, 220]])
print(pred)
