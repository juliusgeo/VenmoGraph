# VenmoGraph
## Purpose
This package was created to allow visualization of relationships between different Venmo users by using their transaction data. It creates a graph data structure where each of the edges between two nodes (users) has a weight that is the number of transactions between those two users. It then does the same thing for the most recent people that the original user has transacted. I am probably going to change it in the future such that it will only map out those other users with the greatest number of common transactions.

## Usage
Make sure that you have NetworkX installed, get an API key and replace the value of "api_access_token" in the script, and then run the script. It will prompt you for a venmo username, and then will output a graph.

## To-do
* Better recursion logic
* Automatic login so the user doesn't have to retrieve API key themselves. 
