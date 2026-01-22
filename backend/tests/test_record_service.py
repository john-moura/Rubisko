import pytest
from unittest.mock import MagicMock, patch
import os
from record_service import update_record, save_file, save_analysis_to_db
from models import Batch, QCRecord, db

def test_update_record_success(app, session):
    """Test updating an existing record"""
    # Create a batch and record
    batch = Batch(code="b1", name="Batch 1", batch_date="2026-01-01T00:00:00Z")
    session.add(batch)
    session.commit()
    
    record = QCRecord(
        batch_id=batch.id,
        date="2026-01-01T10:00:00Z",
        technician="Tech A",
        contamination="No",
        quality_scoring=8,
        developmental_stage="Inconclusive"
    )
    session.add(record)
    session.commit()
    
    # Update
    update_data = {"technician": "Tech B", "qualityScoring": 9}
    result = update_record(record.id, update_data)
    
    # Verify
    assert result["technician"] == "Tech B"
    assert result["qualityScoring"] == 9
    
    # Verify DB
    updated_record = db.session.get(QCRecord, record.id)
    assert updated_record.technician == "Tech B"

def test_update_record_not_found(app, session):
    """Test updating a non-existent record"""
    result = update_record(999, {"technician": "No One"})
    assert result is None

@patch('uuid.uuid4')
def test_save_file(mock_uuid):
    """Test file saving logic with mocked uuid and file object"""
    mock_uuid.return_value = 'test-uuid'
    mock_file = MagicMock()
    mock_file.filename = "image.jpg"
    
    upload_folder = "/fake/uploads"
    
    with patch('os.path.join', side_effect=os.path.join): # Keep os.path.join working
        unique_name, perm_path = save_file(mock_file, upload_folder)
    
    assert unique_name == "test-uuid.jpg"
    assert perm_path == os.path.join(upload_folder, "test-uuid.jpg")
    mock_file.save.assert_called_once_with(perm_path)

def test_save_analysis_to_db(app, session):
    """Test saving a new analysis record to the database"""
    # Create batch
    batch = Batch(code="b2", name="Batch 2", batch_date="2026-01-02T00:00:00Z")
    session.add(batch)
    session.commit()
    
    analysis_result = {
        "technician": "AI Analyst",
        "contamination": "Yes",
        "contaminant": "Bacteria",
        "qualityScoring": 4,
        "developmentalStage": "Germination",
        "biologicalSexRatio": "null",
        "comment": "Sample looks contaminated."
    }
    unique_filename = "abc-123.png"
    
    # Mock request context for host_url
    with app.test_request_context(base_url="http://testserver:5001"):
        result = save_analysis_to_db(batch.id, analysis_result, unique_filename)
        
    # Verify result
    assert result["imageUrl"] == "http://testserver:5001/api/uploads/abc-123.png"
    assert "date" in result
    
    # Verify DB
    record = QCRecord.query.filter_by(batch_id=batch.id).first()
    assert record.technician == "AI Analyst"
    assert record.image_url == "http://testserver:5001/api/uploads/abc-123.png"
