import unittest
from unittest.mock import MagicMock, patch
import json
from analysis_service import parse_analysis_json, analyze_media

class TestAnalysisService(unittest.TestCase):

    def test_parse_analysis_json_clean(self):
        """Test parsing a clean JSON string"""
        raw_json = '{"technician": "Reiss Jones", "qualityScoring": 8}'
        result = parse_analysis_json(raw_json)
        self.assertEqual(result["technician"], "Reiss Jones")
        self.assertEqual(result["qualityScoring"], 8)

    def test_parse_analysis_json_with_markdown(self):
        """Test parsing JSON wrapped in markdown code blocks"""
        raw_json = 'Some intro text\n```json\n{"technician": "Reiss Jones", "qualityScoring": 9}\n```\nSome outro.'
        result = parse_analysis_json(raw_json)
        self.assertEqual(result["qualityScoring"], 9)

    def test_parse_analysis_json_with_raw_markdown(self):
        """Test parsing JSON wrapped in generic markdown backticks"""
        raw_json = '```\n{"technician": "Reiss Jones", "qualityScoring": 7}\n```'
        result = parse_analysis_json(raw_json)
        self.assertEqual(result["qualityScoring"], 7)

    def test_parse_analysis_json_malformed_fallback(self):
        """Test parsing when backticks are messed up but braces exist"""
        raw_json = 'The result is {"technician": "Reiss Jones", "qualityScoring": 10} hope this helps.'
        result = parse_analysis_json(raw_json)
        self.assertEqual(result["qualityScoring"], 10)

    @patch('analysis_service.genai.Client')
    def test_analyze_media_success(self, mock_client_class):
        """Test the full analyze_media flow with mocked Gemini API"""
        # Mock setup
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        
        # Mock file upload response
        mock_file = MagicMock()
        mock_file.state.name = "ACTIVE"
        mock_file.name = "files/test-file-id"
        mock_client.files.upload.return_value = mock_file
        mock_client.files.get.return_value = mock_file
        
        # Mock model generation response
        mock_response = MagicMock()
        mock_response.text = '{"technician": "Reiss Jones", "qualityScoring": 8, "contamination": "No", "developmentalStage": "Germination", "biologicalSexRatio": "50/50"}'
        mock_client.models.generate_content.return_value = mock_response
        
        # Execute
        result_text = analyze_media("fake/path.jpg", "fake-api-key")
        
        # Verify
        self.assertIn('"qualityScoring": 8', result_text)
        mock_client.files.upload.assert_called_once()
        mock_client.models.generate_content.assert_called_once()

    @patch('analysis_service.genai.Client')
    @patch('time.sleep', return_value=None) # Speed up tests
    def test_analyze_media_processing_wait(self, mock_sleep, mock_client_class):
        """Test that it waits for processing state"""
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        
        # First call returns PROCESSING, second returns ACTIVE
        mock_file_proc = MagicMock()
        mock_file_proc.state.name = "PROCESSING"
        
        mock_file_ready = MagicMock()
        mock_file_ready.state.name = "ACTIVE"
        
        mock_client.files.upload.return_value = mock_file_proc
        mock_client.files.get.side_effect = [mock_file_ready]
        
        mock_response = MagicMock()
        mock_response.text = '{"status": "ok"}'
        mock_client.models.generate_content.return_value = mock_response
        
        analyze_media("fake/path.jpg", "fake-api-key")
        
        self.assertEqual(mock_client.files.get.call_count, 1)
        mock_sleep.assert_called_once_with(2)

if __name__ == '__main__':
    unittest.main()
