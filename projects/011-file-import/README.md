# File Import

Implement a service that runs each 5 minutes, and import some data within a set of files to a running database.

In the `samples/files` folder, you'll find a set of folder numbered from 1 to 10.

Each folder simulates a set of files that should be imported.

Before starting the project, you need to import the database schema that you find into the `db/structure.sql` file, into a MySql database

## Task 1

Move the content of the first not-empty folder to a `working` directory

Ex.

On the first attempt, you would work on the `1` folder content
On the second attempt, you should use folder `2` and so on on the other attempts


## Task 2

On each run, compute the files by this specific order:

- storages
- agents
- categories
- clients
- clientsAddresses
- lists
- products
- stocks

Each file respects a specific schema, you cand find it into the `samples/schema` folder


Foreach file:

- check that the structure respects the one expected
- export the data from the file, eventually convert them, and then write the necessary queries to import them into the database