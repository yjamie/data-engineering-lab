from ingestion.extractors.api_extractor import APIExtractor
from ingestion.extractors.csv_extractor import CSVExtractor
from ingestion.connectors.snowflake_connector import SnowflakeConnector
from ingestion.extractors.xlsx_extractor import XLSXExtractor


def main():
    api_connector = APIExtractor(url="")
    csv_connector = CSVExtractor(file_path="")
    xlsx_connector = XLSXExtractor(file_path="")
    database_connector = SnowflakeConnector()


if __name__ == '__main__':
    main()