import unittest

from app.connectors.base import ConnectorConfig
from app.connectors.file_connector import FileConnector
from app.connectors.sql_connector import SQLConnector


class ConnectorTests(unittest.TestCase):
    def test_sql_connector_returns_rows(self):
        connector = SQLConnector(ConnectorConfig(name="analytics", connector_type="sql"))
        connector.connect()
        result = connector.fetch("SELECT 1")

        self.assertEqual(result.metadata["connector_type"], "sql")
        self.assertTrue(result.rows)
        connector.close()

    def test_file_connector_returns_metadata_for_existing_path(self):
        connector = FileConnector(
            ConnectorConfig(name="sample", connector_type="file", source_path="README.md")
        )
        connector.connect()
        result = connector.fetch()

        self.assertEqual(result.metadata["connector_type"], "file")
        self.assertTrue(result.rows)
        connector.close()


if __name__ == "__main__":
    unittest.main()
