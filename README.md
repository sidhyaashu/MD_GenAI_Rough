### Code Summary: Define the Vector Search Index in a JSON file using CLI

```plaintext
Define the Vector Search Index in a JSON file:

Define the data and collection you want to index. Designate the type as vectorSearch and create a name that allows you to easily identify the purpose of the index. Finally, define the fields being indexed, and specify the type, number of dimensions, and similarity.

{
  "database": "sample_mflix",
  "collectionName": "movies",
  "type": "vectorSearch",
  "name": "movies_vector_index",
  "fields": [
    {
      "type": "vector",
      "path": "embedding",
      "numDimensions": 1536,
      "similarity": "cosine"
    }
  ]
}


Create the Index:

Use atlas clusters search indexes create to create the index using a JSON file like the example above. You’ll need to pass in the name of the cluster and the path to the file. Note that depending on how you authenticate, you may need to first specify the appropriate projectID.

atlas clusters search indexes create \
    --clusterName vector \
    --file index.json<?code>


Confirmation

Successful creation of the index should return a confirmation message like this:

Index movies_vector_index created.


Checking Your Indexes:

To check on the status of an index (or multiple indexes) you can use the atlas clusters search indexes list command. You’ll need to specify the names of the cluster, database, and collection for the index. In this example, we are requesting that the output be formatted in JSON.

atlas clusters search indexes list \
    --clusterName vector \
    --db test_mflix \
    --collection movies \
    --output json


This will return an array which will include information on each index within the specified collection.

[
  {
    "collectionName": "movies",
    "database": "test_mflix",
    "indexID": "66720dec75b489672353910b",
    "name": "movies_vector_index",
    "status": "STEADY",
    "type": "vectorSearch",
    "fields": [
      {
        "numDimensions": 1536,
        "path": "embedding",
        "similarity": "cosine",
        "type": "vector"
      }
    ]
  }
]


Looking Up a Specific Index

To see information for a specific index, you can use the atlas clusters search indexes describe command and pass in the index ID, like so:

atlas clusters search indexes describe <id_placeholder> \
    --clusterName vector \
    --output json


This will return information about the index specified. Note that this is a single document, and not an array.

{
  "collectionName": "movies",
  "database": "test_mflix",
  "indexID": "66720dec75b489672353910b",
  "name": "movies_vector_index",
  "status": "STEADY",
  "type": "vectorSearch",
  "fields": [
    {
      "numDimensions": 1536,
      "path": "embedding",
      "similarity": "cosine",
      "type": "vector"
    }
  ]
}


Updating an Existing Index:

Here, we’ve added a filter to the index definition JSON file:

{
  "database": "test_mflix",
  "collectionName": "movies",
  "type": "vectorSearch",
  "name": "movies_vector_index",
  "fields": [
    {
      "type": "vector",
      "path": "embedding",
      "numDimensions": 1536,
      "similarity": "cosine"
    },
    {
      "type": "filter",
      "path": "year"
    }
  ]
}


We can then use the atlas clusters search indexes update command to overwrite the existing index (specified via the indexID) with the new definition:

atlas clusters search indexes update <id_placeholder> \
    --clusterName vector \
    --file index.json \
    --output json


The confirmation message will look like this:

{
  "collectionName": "movies",
  "database": "test_mflix",
  "indexID": "66720dec75b489672353910b",
  "name": "movies_vector_index",
  "status": "IN_PROGRESS",
  "type": "vectorSearch",
  "fields": [
    {
      "numDimensions": 1536,
      "path": "embedding",
      "similarity": "cosine",
      "type": "vector"
    },
    {
      "path": "year",
      "type": "filter"
    }
  ]
}


Note that the filter we added to the JSON definition file is now included in the index, and that the status is listed as “IN_PROGRESS”. This will change to “STEADY” when it is finished being rebuilt. Queries which would benefit from the index will continue to use the original version until the update is complete.

Deleting an Index:

To delete an index use the atlas clusters search indexes delete command. You’ll need to specify the indexID and the name of the cluster the index resides on.

atlas clusters search indexes delete <id_placeholder> \
    --clusterName vector


After running the command, you’ll be prompted to enter y to confirm the deletion, and you will receive a confirmation message:

? Are you sure you want to delete: <id_placeholder> (y/N) y
Index '<id_placeholder>' deleted


You may confirm the deletion of the index by running the atlas clusters search indexes list command:

atlas clusters search indexes list \
    --clusterName vector \
    --db test_mflix \
    --collection movies \
    --output json





```


### Code Summary: Creating a Vector Search Index Using MongoDB Shell
```plaintext

Creating a Vector Search Index Using MongoDB Shell:

Use the db.collection.createSearchIndex command to build an index on a collection. You must specify the type of index as vectorSearch, and you will need to define the fields you wish to index, including the type, number of dimensions, and similarity.

db.movies.createSearchIndex(
  "movies_vector_index", 
  "vectorSearch", 
  {
    "fields": [
      {
        "type": "vector",
        "numDimensions": 1536,
        "path": "plot_embedding",
        "similarity": "cosine",
      }
    ],
  }
);


After running the command, you will receive a confirmation message with the name of the new index:

movies_vector_index


Viewing an Existing Index:

Use the db.collection.getSearchIndexes command and leave it blank in order to see all indexes on the specified collection:

db.movies.getSearchIndexes();


If you wish to specify a particular index, pass in the name of the index as an argument:

db.movies.getSearchIndexes("movies_vector_index");


This will return a lot of information about the index, including the status, which will let you know if the index is ready or still being prepared. It will also show the current definition of the index.

[
  {
    id: "6671e934b362ed3c6ad84512",
    name: "movies_vector_index",
    type: "vectorSearch",
    status: "READY",
    queryable: true,
    latestDefinitionVersion: { version: 0, createdAt: ISODate("2024-06-18T20:08:20.678Z") },
    latestDefinition: {
      fields: [
        {
          type: "vector",
          numDimensions: 1536,
          path: "plot_embedding",
          similarity: "cosine"
        },
      ],
    },
    statusDetail: [
      . . .
    ],
  },
];


Note the statusDetail array in the above example. This array contains an index status array for each node in the cluster.

[
  {
    . . .
    statusDetail: [
      {
        hostname: "atlas-11yyiw-shard-00-02",
        status: "READY",
        queryable: true,
        mainIndex: {
          status: "READY",
          queryable: true,
          definitionVersion: {
            version: 0,
            createdAt: ISODate("2024-06-18T20:08:20.000Z"),
          },
          definition: { fields: [[Object]] },
        },
      },
      . . .
    ]
  },
];


Editing an Existing Vector Search Index:

Update the definition of an existing vector search index with the db.collection.updateSearchIndex command. In this example, we’ll add a filter on the year field.

db.movies.updateSearchIndex(
  "movies_vector_index", 
  {
    "fields": [
      {
        "type": "vector",
        "numDimensions": 1536,
        "path": "embedding",
        "similarity": "cosine",
      },
      {
        "type": "filter",
        "path": "year",
      }
    ],
  }
);


Using db.movies.getSearchIndexes("movies_vector_index"), we can confirm that the update was successful:

[
  {
    id: "6671e934b362ed3c6ad84512",
    name: "movies_vector_index",
    type: "vectorSearch",
    status: "READY",
    queryable: true,
    latestDefinitionVersion: { version: 1, createdAt: ISODate("2024-06-18T20:08:25.348Z") },
    latestDefinition: {
      fields: [
        {
          type: "vector",
          numDimensions: 1536,
          path: "plot_embedding",
          similarity: "cosine"
        },
     { type: 'filter', path: 'year' }
      ],
    },
    statusDetail: [
      . . .
    ],
  },
];


Deleting a Vector Search Index

Delete a vector search index with the db.collection.dropSearchIndex command and pass the name of the vector along as an argument:

db.movies.dropSearchIndex("movies_vector_index");


Running this command will not produce any feedback from the console, so to confirm that the deletion was successful, you can use the db.collection.getSearchIndexes command:

db.movies.getSearchIndexes("movies_vector_index");


This will return the information we’re accustomed to seeing when we run this command. In this case, we can see that the status is listed as “DELETING”, so we know the deletion was successful. We can also run getSearchIndexes again later without specifying an index name, and see that it is no longer present on the collection.

[
  {
    id: "6671e934b362ed3c6ad84512",
    name: "movies_vector_index",
    type: "vectorSearch",
    status: "DELETING",
    queryable: true,
    latestDefinitionVersion: { version: 1, createdAt: ISODate("2024-06-18T20:08:25.348Z") },
    latestDefinition: {
      fields: [
        {
          type: "vector",
          numDimensions: 1536,
          path: "plot_embedding",
          similarity: "cosine"
        },
     { type: 'filter', path: 'year' }
      ],
    },
    statusDetail: [
      . . .
    ],
  },
];

```