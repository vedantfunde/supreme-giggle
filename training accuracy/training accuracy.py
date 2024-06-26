import numpy as np
from sklearn.neighbors import NearestNeighbors
import matplotlib.pyplot as plt

#loading the extracted features
extracted_features = np.load('extracted_features.npy')


#function to retrieve similar images based on a query image
def retrieve_similar_images(query_image_features, k=5):
    #predicting the category of the query image using the decision tree
    predicted_label = decision_tree.predict([query_image_features])[0]

    #finding indices of images with the predicted label
    similar_indices = [i for i, label in enumerate(labels) if label == predicted_label]

    #using Nearest Neighbors to find k similar images based on their features
    nn_model = NearestNeighbors(n_neighbors=k)
    nn_model.fit(extracted_features[similar_indices])
    distances, indices = nn_model.kneighbors([query_image_features])

    #returning the indices of similar images
    return [similar_indices[i] for i in indices[0]]

#function to visualize retrieved images
def visualize_retrieved_images(query_image_index, similar_image_indices):
    plt.figure(figsize=(10, 5))
    plt.subplot(1, len(similar_image_indices) + 1, 1)
    plt.imshow(stored_data[query_image_index][b'R'])
    plt.title('Query Image')
    plt.axis('off')

    for i, index in enumerate(similar_image_indices):
        plt.subplot(1, len(similar_image_indices) + 1, i + 2)
        plt.imshow(stored_data[index][b'R'])
        plt.title('Similar Image {}'.format(i + 1))
        plt.axis('off')

    plt.show()

# Select a subset of query images (e.g., first 5 images)
num_query_images = 10
query_indices = range(num_query_images)

# Visualize retrieved images for each query image
for query_index in query_indices:
    query_image_features = extracted_features[query_index]
    similar_image_indices = retrieve_similar_images(query_image_features)
    visualize_retrieved_images(query_index, similar_image_indices)

# Function to calculate accuracy
def calculate_accuracy():
    correct_predictions = 0
    total_predictions = 0

    for i in range(len(extracted_features)):
        query_image_features = extracted_features[i]
        similar_image_indices = retrieve_similar_images(query_image_features)

        # Get ground truth label for the query image
        query_image_label = labels[i]

        # Get predicted labels for the retrieved images
        predicted_labels = [labels[index] for index in similar_image_indices]

        # Check if the ground truth label is in the predicted labels
        if query_image_label in predicted_labels:
            correct_predictions += 1

        total_predictions += 1

    accuracy = correct_predictions / total_predictions
    return accuracy

# Calculate accuracy
accuracy = calculate_accuracy()
#print("Accuracy:", accuracy)
