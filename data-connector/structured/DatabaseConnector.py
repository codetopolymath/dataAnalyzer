import DataConnector
from DataConnector import ConnectorStatus

from typing import List, Dict, Any
from enum import Enum

class DatabaseConnector(DataConnector):

    class DatabaseType(Enum):
        MYSQL = "mysql"
        POSTGRES = "postgres"
        SQLITE = "sqlite"
        ORACLE = "oracle"
        MSSQL = "mssql"
        MONGODB = "mongodb"
        REDIS = "redis"
        NEO4J = "neo4j"
        COUCHBASE = "couchbase"
        COUCHDB = "couchdb"
        ELASTICSEARCH = "elasticsearch"
        INFLUXDB = "influxdb"
        CASSANDRA = "cassandra"
        DYNAMODB = "dynamodb"
        FIREBASE = "firebase"
        BIGQUERY = "bigquery"
        SNOWFLAKE = "snowflake"
        REDSHIFT = "redshift"
        OTHER = "other"

    def connect(self) -> bool:
        try:
            # Implement database-specific connection logic
            connection_string = self.config["data_source"]["database"][0]
            self.database_type = self.get_database_type(connection_string)
            self.connection = self.create_database_connection(connection_string)
            self.status = ConnectorStatus.CONNECTED
            return True
        except Exception as e:
            self.logger.error(f"Error connecting to database: {str(e)}")
            self.status = ConnectorStatus.FAILED
            return False

    def fetch_data(self) -> List[Dict[str, Any]]:
        super().fetch_data()  # parent fetch_data method contains connection check
        # IMPLIMENT DATABASE SPECIFIC DATA FETCHING LOGIC
        return []

    def disconnect(self) -> None:
        if self.connection:
            self.connection.close()
            self.status = ConnectorStatus.DISCONNECTED


    # DATABASE_SPECIFIC METHODS

    def get_database_type(self, connection_string: str) -> DatabaseType:

        ''' Determine the type of database from the connection string
        Args:
            connection_string (str): Connection string of the database
        Returns:
            DatabaseType: Type of the database [ENUM]
        '''

        db_type_map = {
            "mysql": self.DatabaseType.MYSQL,
            "postgres": self.DatabaseType.POSTGRES,
            "sqlite": self.DatabaseType.SQLITE,
            "oracle": self.DatabaseType.ORACLE,
            "mssql": self.DatabaseType.MSSQL,
            "mongodb": self.DatabaseType.MONGODB,
            "redis": self.DatabaseType.REDIS,
            "neo4j": self.DatabaseType.NEO4J,
            "couchbase": self.DatabaseType.COUCHBASE,
            "couchdb": self.DatabaseType.COUCHDB,
            "elasticsearch": self.DatabaseType.ELASTICSEARCH,
            "influxdb": self.DatabaseType.INFLUXDB,
            "cassandra": self.DatabaseType.CASSANDRA,
            "dynamodb": self.DatabaseType.DYNAMODB,
            "firebase": self.DatabaseType.FIREBASE,
            "bigquery": self.DatabaseType.BIGQUERY,
            "snowflake": self.DatabaseType.SNOWFLAKE,
            "redshift": self.DatabaseType.REDSHIFT
        }
        for prefix, db_type in db_type_map.items():
            if connection_string.startswith(prefix):
                return db_type
        return self.DatabaseType.OTHER

    def create_database_connection(self, connection_string: str) -> Any:
        if self.database_type == self.DatabaseType.MYSQL:
            return self.create_mysql_connection(connection_string)
