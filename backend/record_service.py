from models import db, QCRecord
import os
import uuid
from datetime import datetime, timezone

def update_record(record_id, data):
    """
    Updates an existing QC record with the provided data.
    Returns the updated record to_dict or None if not found.
    """
    record = db.session.get(QCRecord, record_id)
    if not record:
        return None
    
    # Update fields if provided in the data dictionary
    if 'technician' in data: 
        record.technician = data['technician']
    if 'contamination' in data: 
        record.contamination = data['contamination']
    if 'contaminant' in data: 
        record.contaminant = data['contaminant']
    if 'qualityScoring' in data: 
        record.quality_scoring = data['qualityScoring']
    if 'developmentalStage' in data: 
        record.developmental_stage = data['developmentalStage']
    if 'biologicalSexRatio' in data: 
        record.biological_sex_ratio = data['biologicalSexRatio']
    if 'comment' in data: 
        record.comment = data['comment']
    
    db.session.commit()
    return record.to_dict()

def save_file(file, upload_folder):
    """Save the uploaded file permanently with a unique name"""
    file_ext = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    perm_path = os.path.join(upload_folder, unique_filename)
    file.save(perm_path)
    return unique_filename, perm_path

def save_analysis_to_db(batch_id, analysis_result, unique_filename):
    """Persists the final record to the database"""
    # Add timestamp
    current_time = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    analysis_result['date'] = current_time
    
    # Define image URL
    from flask import request
    base_url = request.host_url.rstrip('/')
    image_url = f"{base_url}/api/uploads/{unique_filename}"
    
    new_record = QCRecord(
        batch_id=batch_id,
        date=analysis_result['date'],
        technician=analysis_result['technician'],
        contamination=analysis_result['contamination'],
        contaminant=analysis_result.get('contaminant'),
        quality_scoring=analysis_result['qualityScoring'],
        developmental_stage=analysis_result['developmentalStage'],
        biological_sex_ratio=analysis_result['biologicalSexRatio'],
        comment=analysis_result.get('comment'),
        image_url=image_url
    )
    db.session.add(new_record)
    db.session.commit()
    
    # Return augmented results for the frontend
    analysis_result['imageUrl'] = image_url
    return analysis_result
