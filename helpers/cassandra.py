from datetime import timedelta

import pandas as pd
from cassandra.cluster import Cluster

from logger import Logger


class CassandraInterface(object):
    def __init__(self, ip_address, port=9042, key_space=None, table_name=None):
        self.ip_address = ip_address if isinstance(ip_address, list) else [ip_address]
        self.port = port
        self.key_space = key_space
        self.key_space_changed = False
        self.table_name = table_name
        self.session = None

        self.logger = Logger(self.__class__.__name__).get()

    @property
    def key_space(self):
        return self.__key_space

    @key_space.setter
    def key_space(self, key_space):
        self.key_space_changed = True
        self.__key_space = key_space

    @property
    def table_name(self):
        return self.__key_space

    @table_name.setter
    def table_name(self, table_name):
        self.__table_name = table_name

    def _connect_to_db(self):
        """
        Achieve a connection to the cassandra db, private method
        :return: A cassandra DB session object
        """
        cluster = Cluster(self.ip_address, self.port)
        session = cluster.connect(self.key_space)
        self.logger.info(
            f"Successfully connected to cluster with {self.key_space if self.key_space else 'no'} keyspace"
        )
        return session

    def connect_to_db(self):
        """
        Public interface (crude singleton) for database connection with Cassandra DB
        :return: A cassandra DB session object
        """
        if not self.session:
            self.session = self._connect_to_db()
        if self.key_space_changed:
            self.session.set_keyspace(self.key_space)
        return self.session

    def retrieve_with_timestamps(
        self, start_timestamp, end_timestamp, remove_tzinfo=True
    ):
        """
        Make a cql selection query in the cassandra
        remove_tzinfo if set to true will convert the retrieved values to local timezone
        :param start_timestamp: start timestamp as datetime.datetime() object
        :param end_timestamp: end timestamp as datetime.datetime() object
        :param remove_tzinfo: if true then remove the timezone info
        :return: pd.DataFrame with sorted dates exclusive of both timestamps
        """
        session = self.connect_to_db()
        rows = session.execute(
            f"SELECT * FROM {self.table_name} WHERE key<'{end_timestamp}' and key>'{start_timestamp}' ALLOW FILTERING;"
        )
        if not rows:
            raise ValueError("No rows were returned from the database")
        df = pd.DataFrame(list(rows))

        if remove_tzinfo:
            df["key"] = df["key"].replace(tzinfo=None)
        df.sort_values(by=["key"], inplace=True)
        return df

    def get_last_timestamp(self):
        """
        Get the last timestamp existing in the database
        :return: max(date_index)
        """
        session = self.connect_to_db()
        rows = session.execute(f"SELECT * FROM {self.table_name};")
        if not rows:
            raise ValueError("No rows were returned from the database")
        df = pd.DataFrame(list(rows))
        return df["key"].max().replace(tzinfo=None)

    def write_rows(self, start_timestamp, pred_steps, predictions):
        """
        Writes rows to Cassandra DB
        :param start_timestamp:
        :param pred_steps:
        :param predictions: Predictions from the forecasting engine
        :return: None
        """
        session = self.connect_to_db()
        for i in range(pred_steps):
            session.execute(
                f"INSERT INTO {self.table_name} (key, value) VALUES"
                f" ('{start_timestamp + timedelta(seconds=i)}', {predictions[i]});"
            )

    def _create_key_space(self, new_key_space_name, config_dict=None):
        if not config_dict:
            config_dict = {"class": "SimpleStrategy", "replication_factor": 3}
        query = f"CREATE KEYSPACE IF NOT EXISTS {new_key_space_name} WITH REPLICATION = {str(config_dict)};"
        session = self.connect_to_db()
        try:
            session.execute(query)
        except Exception as e:
            self.logger.error(str(e))
            raise e
        print(
            "Please update the key_space using `object.key_space = new_key_space_name` \n"
            "if you want to start using the created keyspace."
        )
        self.logger.info(f"Successfully created keyspace {new_key_space_name}")

    def _drop_key_space(self, key_space_name):
        if self.key_space == key_space_name:
            raise ValueError(
                "Keyspace {key_space_name} is in use. Please set it to `None` before trying to drop it."
            )
        query = f"DROP KEYSPACE {key_space_name};"
        self.connect_to_db().execute(query)
        self.logger.info(f"Successfully dropped keyspace {key_space_name}")

    def _create_table(self, new_table_name, schema, primary_key_cols):
        # Create a schema string like 'key timestamp, id text, value double'
        schema_string = ", ".join(
            [
                "".join([column_name, " ", column_type])
                for column_name, column_type in schema.items()
            ]
        )
        # Add which keys are primary keys to the schema string
        add_primary_keys = schema_string + f", PRIMARY KEY ({', '.join(list(primary_key_cols))})"
        query = f"CREATE TABLE {new_table_name} ({add_primary_keys})"
        self.connect_to_db().execute(query)
        self.logger.info(f"Successfully dropped table {new_table_name}")