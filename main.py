from ingestion.connectors.api_connector import APIConnector
from ingestion.connectors.csv_connector import CSVConnector
from ingestion.connectors.database_connector import DatabaseConnector
from ingestion.connectors.xlsx_connector import XLSXConnector


def main():
    api_connector = APIConnector(url="")
    csv_connector = CSVConnector(file_path="")
    xlsx_connector = XLSXConnector(file_path="")
    database_connector = DatabaseConnector()


if __name__ == '__main__':
    main()