import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from scipy.spatial.distance import euclidean

data = np.array([
    [100, 2], [250, 5], [700, 10], [50, 1], [1800, 3],
    [900, 12], [120, 7], [1600, 2], [60, 15], [1100, 8]
])

kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
kmeans.fit(data)
labels = kmeans.labels_
centroids = kmeans.cluster_centers_

print("Cluster Centers (Spending, Visits):")
for idx, centroid in enumerate(centroids):
    print(f"Cluster {idx}: {centroid}")

def customer_define(spending, visits):
    point = np.array([spending, visits])
    distances = [euclidean(point, centroid) for centroid in centroids]
    assigned_cluster = np.argmin(distances)
    print(f"Customer assigned to Cluster {assigned_cluster}")
    return assigned_cluster


spend = float(input("Enter spending: "))
visit = int(input("Enter website visit: "))
customer_define(spend,visit)

plt.scatter(data[:, 0], data[:, 1], c=labels, cmap='viridis', marker='o')
plt.scatter(centroids[:, 0], centroids[:, 1], c='red', marker='x', s=200, label='Centroids')
plt.xlabel('Monthly Spending (USD)')
plt.ylabel('Number of Website Visits')
plt.title('Customer Segmentation using K-Means')
plt.legend()
plt.show()

