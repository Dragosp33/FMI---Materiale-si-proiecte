def levenshtein_distance(word1, word2):
    m = len(word1)
    n = len(word2)
    
    # Create a matrix to store the distances
    distances = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Initialize the first row and column of the matrix
    for i in range(m + 1):
        distances[i][0] = i
    for j in range(n + 1):
        distances[0][j] = j
    
    # Calculate the distances
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                distances[i][j] = distances[i - 1][j - 1]
            else:
                substitute_cost = distances[i - 1][j - 1]
                insert_cost = distances[i][j - 1]
                delete_cost = distances[i - 1][j]
                distances[i][j] = min(substitute_cost, insert_cost, delete_cost) + 1
    
    return distances[m][n]

# Example usage
word1 = "kitten"
word2 = "sitting"
distance = levenshtein_distance(word1, word2)
print(f"The Levenshtein distance between '{word1}' and '{word2}' is: {distance}")