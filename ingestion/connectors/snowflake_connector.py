import logging
import pandas as pd
import snowflake.connector

from ingestion.connectors.base_connector import BaseConnector

logger = logging.getLogger(__name__)

class SnowflakeConnector(BaseConnector):
    """Handles connection management, authentication, and disconnection for Snowflake database"""

    def __init__(
            self,
            user:str,
            password:str,
            account:str,
            database:str = None,
            schema:str = None,
            warehouse:str = None,
            role:str = None
    ):
        self.user = user
        self.password = password
        self.account = account
        self.database = database
        self.schema = schema
        self.warehouse = warehouse
        self.role = role
        self.connection = None

    def connect(self) -> None:
        """Establishes connection to Snowflake"""
        if self.is_connected():
            logger.info("Already connected to Snowflake")
            return

        logger.info("Starting Snowflake connection")

        try:
            self.connection = snowflake.connector.connect(
                user=self.user,
                password=self.password,
                account=self.account,
                database=self.database,
                schema=self.schema,
                warehouse=self.warehouse,
                role=self.role
            )
            logger.info("Successfully connected to Snowflake")
        except snowflake.connector.errors.Error:
            logger.exception("Failed to connect to Snowflake")
            self.connection = None
            raise


    def disconnect(self) -> None:
        """Disconnects Snowflake connection"""
        if self.connection is not None:
            logger.info("Begin disconnecting Snowflake connection")
            try:
                # In case the connection was closed outside of disconnect()
                if not self.connection.is_closed():
                    self.connection.close()
            finally:
                self.connection = None

    def is_connected(self) -> bool:
        """Checks if connection object exists and connection is not closed"""
        return not(self.connection is None or self.connection.is_closed())

    def execute_query(self, query:str, params=None) -> dict:
        """Executes SQL query (INSERT, CREATE, UPDATE, DELETE, etc.) and returns query metadata"""
        if not self.is_connected():
            raise RuntimeError("Snowflake connector is not connected")

        logger.info("Executing Snowflake SQL query")

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)

                metadata = {
                    "query_id": cursor.sfqid,
                    "row_count": cursor.rowcount
                }

                logger.info("Query completed. Query ID: %s, Rows affected: %s",
                            metadata["query_id"], metadata["row_count"])

                return metadata
        except snowflake.connector.errors.Error:
            logger.exception("Failed to execute SQL query")
            raise


    def fetch_results(self,query:str, params=None) -> pd.DataFrame:
        """Executes SELECT query. Returns a DataFrame with results"""
        if not self.is_connected():
            raise RuntimeError("Snowflake connector is not connected")

        logger.info("Fetching results from Snowflake")

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                df = cursor.fetch_pandas_all()
                logger.info("Successfully fetched %d rows. Query ID: %s", len(df), cursor.sfqid)
                return df
        except snowflake.connector.errors.Error:
            logger.exception("Failed to execute SQL query")
            raise

    def __validate_query(self, query):
        """
        Validates a query before execution by checking its structure, required permissions, and access rights.
        Raises:
            PermissionError: If user does not have required permissions
            ValueError: If query has improper format
        """
        pass