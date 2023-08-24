# What is this application?
This application is a process-based discrete event simulator that measures the
movement of trains, the movement of the cargo they carry, the shortest path for
a train to its destination, and the shortest path for cargo to its destination.
The trains must pass through the appropriate stations on the way to its 
destination and the cargo they carry can get dropped off at a station. The 
simulator tests the stress of the system of the train stations by controlling
the number of active trains, how many trains the station can hold, how much 
cargo the stations can hold, and how the system reacts to the rate of new 
appearing cargo.


# How it works
The example files listed (Book1.csv and Georgia.csv) contain the necessary
to setup the program with the information. 

Georgia.csv contains the information of the each station and the ones they
connect to as well.

Book1.csv contains the times it would take to travel to each station. The NaN
value fills up the nonexistant connections between stations. Those won't be
used in the program.

### The Available Arguments to Provide
On the CLI when running the program, you can provide these arguments to adjust
the different aspects of the simulation. There are default ones provided already.

1. '-sc' Starting Cargo: This argument tag allows you to control the amount of
cargo at each station upon initialization. Int required for this arguement.

2. '-seed' Seed: This argument tag allows you to control the randomness of the 
simulation. With this tag, you can recreate specific types of states of 
randomness to test to certain aspects of the simulation. Int required for this
argument

3. '-tc' Train Cargo: This argument tag allows you to control the amount of train
cargo by the train. Int required for this argument.

4. '-stc' Station Cargo Size: This argument tag allows you to control the amount
cargo a train station can hold. Int required for this argument.

5. '-neigh' Neighbors: This argument tag sets up the stations and their neighbors.
Defaults to Georgia.csv, but you can setup your own. String required; needs to be
the name of the csv file.

6. '-times' Times: This argument tag sets up the times required to travel between
the stations. Defaults to Book1.csv, but you can setup your own. String required;
needs to be the name of the csv file.


### I want to run my own train simulation, what do I do?

Easy, using Microsoft excel, you can create two spreadsheets. For the first
spreadsheet, you will need two columns: a column of the names of city, and the 
other should contain a string that the connecting cities. For example, a row 
would look like "| DOV | MIL-MET-SAV |".

For the second spreadsheet, you will need a csv file containing the times that 
would take to travel between the cities. The top row and far-most left column
shoulud contain the names of cities, and the cells in between have the corresponding
cells. There is an example of what the file should look like in the repository.
