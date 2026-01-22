from flask import Blueprint, jsonify, request, send_from_directory, current_app
from models import db, Batch, QCRecord
from analysis_service import analyze_media, parse_analysis_json
from record_service import update_record, save_file, save_analysis_to_db

api_bp = Blueprint('api', __name__)

@api_bp.route('/api/batches', methods=['GET'])
def get_batches():
    """Get all batches"""
    batches = Batch.query.all()
    return jsonify([b.to_dict() for b in batches])

@api_bp.route('/api/batch/<int:batch_id>', methods=['GET'])
def get_batch(batch_id):
    """Get a specific batch detail"""
    batch = Batch.query.get(batch_id)
    if not batch:
        return jsonify({'error': 'Batch not found'}), 404
    return jsonify(batch.to_dict())

@api_bp.route('/api/batch/<int:batch_id>/qc-records', methods=['GET'])
def get_qc_records(batch_id):
    """Get QC records for a specific batch"""
    records = QCRecord.query.filter_by(batch_id=batch_id).order_by(QCRecord.date.desc()).all()
    return jsonify([r.to_dict() for r in records])

@api_bp.route('/api/uploads/<filename>', methods=['GET'])
def get_upload(filename):
    """Serve uploaded files"""
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

@api_bp.route('/api/qc-record/<int:record_id>', methods=['PUT'])
def update_qc_record(record_id):
    """Update an existing QC record"""
    try:
        data = request.json
        updated_data = update_record(record_id, data)
        
        if not updated_data:
            return jsonify({'error': 'Record not found'}), 404
            
        return jsonify({'success': True, 'record': updated_data})
    except Exception as e:
        print(f"Error updating record: {e}")
        return jsonify({'error': str(e)}), 500

@api_bp.route('/api/analyze-qc-image', methods=['POST'])
def analyze_qc_image():
    """Analyze uploaded image/video with Gemini and extract QC data"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        batch_id_raw = request.form.get('batchId', '')
        try:
            batch_id = int(batch_id_raw)
        except (TypeError, ValueError):
            return jsonify({'error': 'Invalid batch ID'}), 400
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        gemini_api_key = current_app.config.get('GEMINI_API_KEY')
        if not gemini_api_key:
            return jsonify({'error': 'Gemini API key not configured'}), 500
        
        # 1. Save file permanently
        unique_filename, file_path = save_file(file, current_app.config['UPLOAD_FOLDER'])
        
        # 2. Analyze with Gemini
        response_text = analyze_media(file_path, gemini_api_key)
        
        # 3. Parse JSON
        analysis_result = parse_analysis_json(response_text)
        
        # 4. Save to DB
        final_result = save_analysis_to_db(batch_id, analysis_result, unique_filename)
        
        print(f"Analysis successful: {final_result}")
        return jsonify({
            'success': True,
            'analysis': final_result
        })
    
    except Exception as e:
        print(f"Error in analysis route: {e}")
        return jsonify({'error': str(e)}), 500
