# pinterest-api

Setup the python environment by using the `requirements.txt` file

`pip install -r requirements.txt`

You start all services (after installation) in different terminals after setting them up.

```
# Start the FAST API server
python API/project_pin_API.py

# Start the event posting script
python User_Emulation/user_posting_emulation.py

# Start zookeeper for kafka connections
zookeeper-server-start /usr/local/etc/kafka/zookeeper.properties

# Start kafka server
kafka-server-start /usr/local/etc/kafka/server.properties

# Start the batch consumer to put data to S3
python Consumers/batch_consumer.py

# Start streaming consumer to put data to Postgresql
python Consumers/streaming_consumer.py
```

`cred_file.ini` contains all necessary access parameters for AWS.

Run the following to get the json files from S3 locally:
```
python helpers/boto_connection.py
```

You can use these local files or use the S3 URI in `batch-spark-cassandra.py` to batch ingest data into Cassandra.

Usage:
`python batch-spark-cassandra.py`

For using Airfow:

We need to copy `airflow_sample.py` file to ~/airflow/dags (default location) after installation

`cp airflow_sample.py ~/airflow/dags/`

Then we need to run the python file from there:

`python ~/airflow/dags/airflow_sample.py `

Use following commands after setting the dag there:

```
# initialize the database tables
airflow db init

# print the list of active DAGs
airflow dags list

# prints the list of tasks in the "tutorial" DAG
airflow tasks list spark

# prints the hierarchy of tasks in the "tutorial" DAG
airflow tasks list spark --tree

# command layout: command subcommand dag_id task_id date

# testing print_date
airflow tasks test spark print_date 2015-06-01

# testing spark batch consumer run test
airflow tasks test spark spark_run 2015-06-01
```

When you setup postgresql, you can use the commands `bash/create_table.sql` to setup the user and the table 
required for the script to run. Do not try running the script, rather run the commands individually inside postgres

The other commands are also saved in `bash/kafka-commands.sh`

