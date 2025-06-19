import pandas as pd

# Define the range of n values
n_values = range(3, 11)

# Create a dictionary to store the data for the table
table_data = {}

# Iterate through each n value
for n in n_values:
    # Dictionary to store the count of solutions for each c
    solution_counts = {}

    # Loop through all values of c from 0 to n-1
    for c in range(n):
        # List to store valid combinations of (x, y)
        solutions = []

        # Iterate over all possible values of x and y in the range [0, 20]
        for x in range(21):
            for y in range(21):
                # Check if the equation is satisfied
                if (x**2 + y**2) % n == c:
                    solutions.append((x, y))

        # Store the count of solutions for the current c
        solution_counts[c] = len(solutions)

    # Add the solution counts for this n to the table data
    table_data[n] = solution_counts

# Convert the table data to a pandas DataFrame
df = pd.DataFrame.from_dict(table_data, orient='index').transpose()

# Fill NaN values with 0 (for c values that don't exist for some n)
df = df.fillna(0).astype(int)

# Print the table
print(df)
