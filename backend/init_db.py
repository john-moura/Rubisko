import json
import os
from app import app
from models import db, Batch, QCRecord

def init_db():
    with app.app_context():
        # Create tables
        db.create_all()
        print("Database tables created.")

        # Paths to JSON files, including seed files
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        base_dir = os.path.join(project_root, 'frontend', 'src', 'data')
        batches_path = os.path.join(base_dir, 'batchDetails.json')
        qc_records_path = os.path.join(base_dir, 'qualityControlRecords.json')

        # Check if database is already populated
        if Batch.query.first():
            print("Database already contains data. Skipping migration.")
            return

        # Load and migrate Batches
        batch_id_map = {}
        if os.path.exists(batches_path):
            with open(batches_path, 'r') as f:
                batches_data = json.load(f)
                for b in batches_data:
                    batch = Batch(
                        code=b['id'],
                        name=b['batchName'],
                        batch_date=b['batchDate']
                    )
                    db.session.add(batch)
                    db.session.flush() # Get the generated ID
                    batch_id_map[b['id']] = batch.id
            print(f"Migrated {len(batches_data)} batches.")
        else:
            print("batchDetails.json not found.")

        # Load and migrate QC Records
        if os.path.exists(qc_records_path):
            with open(qc_records_path, 'r') as f:
                qc_data = json.load(f)
                count = 0
                for legacy_batch_id, records in qc_data.items():
                    real_batch_id = batch_id_map.get(legacy_batch_id)
                    if real_batch_id is None:
                        continue
                        
                    for r in records:
                        qc_record = QCRecord(
                            batch_id=real_batch_id,
                            date=r['date'],
                            technician=r['technician'],
                            contamination=r['contamination'],
                            contaminant=r.get('contaminant'),
                            quality_scoring=r['qualityScoring'],
                            developmental_stage=r['developmentalStage'],
                            biological_sex_ratio=r['biologicalSexRatio'],
                            comment=r.get('comment')
                        )
                        db.session.add(qc_record)
                        count += 1
            print(f"Migrated {count} QC records.")
        else:
            print("qualityControlRecords.json not found.")

        db.session.commit()
        print("Migration complete.")

if __name__ == '__main__':
    init_db()
