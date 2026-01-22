from app import app
from models import db, Batch, QCRecord

BATCHES = [
  {
    "id": "batch_01_2026",
    "batchName": "Seaweed seed - Batch_01_2026",
    "batchDate": "2026-01-01T00:00:00Z"
  },
  {
    "id": "batch_02_2026",
    "batchName": "Seaweed seed - Batch_02_2026",
    "batchDate": "2026-01-06T00:00:00Z"
  },
  {
    "id": "batch_03_2026",
    "batchName": "Seaweed seed - Batch_03_2026",
    "batchDate": "2026-01-08T00:00:00Z"
  },
  {
    "id": "batch_04_2026",
    "batchName": "Seaweed seed - Batch_04_2026",
    "batchDate": "2026-01-12T00:00:00Z"
  },
  {
    "id": "batch_05_2026",
    "batchName": "Seaweed seed - Batch_05_2026",
    "batchDate": "2026-01-13T00:00:00Z"
  },
  {
    "id": "batch_06_2026",
    "batchName": "Seaweed seed - Batch_06_2026",
    "batchDate": "2026-01-16T00:00:00Z"
  }
]

QC_RECORDS = {
  "batch_01_2026": [
    {
      "date": "2026-01-03T09:30:00Z",
      "technician": "Reiss Jones",
      "contamination": "No",
      "contaminant": None,
      "qualityScoring": 8,
      "developmentalStage": "Germination",
      "biologicalSexRatio": "30/70",
      "comment": None
    },
    {
      "date": "2026-01-02T14:15:00Z",
      "technician": "Reiss Jones",
      "contamination": "Yes",
      "contaminant": "bacteria",
      "qualityScoring": 5,
      "developmentalStage": "Spore Release",
      "biologicalSexRatio": "60/40",
      "comment": None
    },
    {
      "date": "2026-01-01T10:45:00Z",
      "technician": "Reiss Jones",
      "contamination": "No",
      "contaminant": None,
      "qualityScoring": 9,
      "developmentalStage": "Zygote Formation",
      "biologicalSexRatio": "30/70",
      "comment": None
    },
    {
      "date": "2026-01-05T11:20:00Z",
      "technician": "Reiss Jones",
      "contamination": "No",
      "contaminant": None,
      "qualityScoring": 9,
      "developmentalStage": "Juvenile Sporophyte Growth",
      "biologicalSexRatio": "70/30",
      "comment": None
    },
    {
      "date": "2026-01-04T15:00:00Z",
      "technician": "Reiss Jones",
      "contamination": "No",
      "contaminant": None,
      "qualityScoring": 10,
      "developmentalStage": "Spore Release",
      "biologicalSexRatio": "70/30",
      "comment": None
    }
  ],
  "batch_02_2026": [
    {
      "date": "2026-01-05T08:45:00Z",
      "technician": "Reiss Jones",
      "contamination": "No",
      "contaminant": None,
      "qualityScoring": 7,
      "developmentalStage": "Germination",
      "biologicalSexRatio": "70/30",
      "comment": None
    },
    {
      "date": "2026-01-09T13:30:00Z",
      "technician": "Reiss Jones",
      "contamination": "Yes",
      "contaminant": "fungi",
      "qualityScoring": 4,
      "developmentalStage": "Spore Release",
      "biologicalSexRatio": "30/70",
      "comment": None
    },
    {
      "date": "2026-01-08T09:15:00Z",
      "technician": "Reiss Jones",
      "contamination": "No",
      "contaminant": None,
      "qualityScoring": 8,
      "developmentalStage": "Zygote Formation",
      "biologicalSexRatio": "60/40",
      "comment": None
    },
    {
      "date": "2026-01-07T14:50:00Z",
      "technician": "Reiss Jones",
      "contamination": "No",
      "contaminant": None,
      "qualityScoring": 8,
      "developmentalStage": "Juvenile Sporophyte Growth",
      "biologicalSexRatio": "60/40",
      "comment": None
    },
    {
      "date": "2026-01-09T10:30:00Z",
      "technician": "Reiss Jones",
      "contamination": "No",
      "contaminant": None,
      "qualityScoring": 9,
      "developmentalStage": "Spore Release",
      "biologicalSexRatio": "30/70",
      "comment": None
    }
  ],
  "batch_03_2026": [
    {
      "date": "2026-01-07T11:00:00Z",
      "technician": "Reiss Jones",
      "contamination": "No",
      "contaminant": None,
      "qualityScoring": 9,
      "developmentalStage": "Germination",
      "biologicalSexRatio": "40/60",
      "comment": None
    },
    {
      "date": "2026-01-09T15:45:00Z",
      "technician": "Reiss Jones",
      "contamination": "No",
      "contaminant": None,
      "qualityScoring": 9,
      "developmentalStage": "Spore Release",
      "biologicalSexRatio": "50/50",
      "comment": None
    },
    {
      "date": "2026-01-08T09:30:00Z",
      "technician": "Reiss Jones",
      "contamination": "Yes",
      "contaminant": "microalgae",
      "qualityScoring": 6,
      "developmentalStage": "Zygote Formation",
      "biologicalSexRatio": "70/30",
      "comment": None
    },
    {
      "date": "2026-01-07T13:15:00Z",
      "technician": "Reiss Jones",
      "contamination": "No",
      "contaminant": None,
      "qualityScoring": 8,
      "developmentalStage": "Juvenile Sporophyte Growth",
      "biologicalSexRatio": "70/30",
      "comment": None
    },
    {
      "date": "2026-01-11T10:00:00Z",
      "technician": "Reiss Jones",
      "contamination": "No",
      "contaminant": None,
      "qualityScoring": 9,
      "developmentalStage": "Spore Release",
      "biologicalSexRatio": "30/70",
      "comment": None
    }
  ],
  "batch_04_2026": [
    {
      "date": "2026-01-11T08:30:00Z",
      "technician": "Reiss Jones",
      "contamination": "No",
      "contaminant": None,
      "qualityScoring": 8,
      "developmentalStage": "Germination",
      "biologicalSexRatio": "60/40",
      "comment": None
    },
    {
      "date": "2026-01-10T14:20:00Z",
      "technician": "Reiss Jones",
      "contamination": "No",
      "contaminant": None,
      "qualityScoring": 9,
      "developmentalStage": "Spore Release",
      "biologicalSexRatio": "30/70",
      "comment": None
    },
    {
      "date": "2026-01-12T11:45:00Z",
      "technician": "Reiss Jones",
      "contamination": "Yes",
      "contaminant": "bacteria",
      "qualityScoring": 5,
      "developmentalStage": "Zygote Formation",
      "biologicalSexRatio": "60/40",
      "comment": None
    },
    {
      "date": "2026-01-11T09:00:00Z",
      "technician": "Reiss Jones",
      "contamination": "No",
      "contaminant": None,
      "qualityScoring": 7,
      "developmentalStage": "Juvenile Sporophyte Growth",
      "biologicalSexRatio": "40/60",
      "comment": None
    },
    {
      "date": "2026-01-10T15:30:00Z",
      "technician": "Reiss Jones",
      "contamination": "No",
      "contaminant": None,
      "qualityScoring": 8,
      "developmentalStage": "Spore Release",
      "biologicalSexRatio": "50/50",
      "comment": None
    }
  ],
  "batch_05_2026": [
    {
      "date": "2026-01-15T10:15:00Z",
      "technician": "Reiss Jones",
      "contamination": "No",
      "contaminant": None,
      "qualityScoring": 9,
      "developmentalStage": "Germination",
      "biologicalSexRatio": "30/70",
      "comment": None
    },
    {
      "date": "2026-01-14T13:45:00Z",
      "technician": "Reiss Jones",
      "contamination": "No",
      "contaminant": None,
      "qualityScoring": 10,
      "developmentalStage": "Spore Release",
      "biologicalSexRatio": "40/60",
      "comment": None
    },
    {
      "date": "2026-01-13T09:20:00Z",
      "technician": "Reiss Jones",
      "contamination": "No",
      "contaminant": None,
      "qualityScoring": 9,
      "developmentalStage": "Zygote Formation",
      "biologicalSexRatio": "60/40",
      "comment": None
    },
    {
      "date": "2026-01-17T14:00:00Z",
      "technician": "Reiss Jones",
      "contamination": "Yes",
      "contaminant": "fungi",
      "qualityScoring": 6,
      "developmentalStage": "Juvenile Sporophyte Growth",
      "biologicalSexRatio": "50/50",
      "comment": None
    },
    {
      "date": "2026-01-16T11:30:00Z",
      "technician": "Reiss Jones",
      "contamination": "No",
      "contaminant": None,
      "qualityScoring": 8,
      "developmentalStage": "Spore Release",
      "biologicalSexRatio": "60/40",
      "comment": None
    }
  ],
  "batch_06_2026": [
    {
      "date": "2026-01-18T08:45:00Z",
      "technician": "Reiss Jones",
      "contamination": "No",
      "contaminant": None,
      "qualityScoring": 8,
      "developmentalStage": "Germination",
      "biologicalSexRatio": "50/50",
      "comment": None
    },
    {
      "date": "2026-01-17T15:15:00Z",
      "technician": "Reiss Jones",
      "contamination": "No",
      "contaminant": None,
      "qualityScoring": 9,
      "developmentalStage": "Spore Release",
      "biologicalSexRatio": "70/30",
      "comment": None
    },
    {
      "date": "2026-01-19T10:30:00Z",
      "technician": "Reiss Jones",
      "contamination": "No",
      "contaminant": None,
      "qualityScoring": 9,
      "developmentalStage": "Zygote Formation",
      "biologicalSexRatio": "50/50",
      "comment": None
    },
    {
      "date": "2026-01-21T13:00:00Z",
      "technician": "Reiss Jones",
      "contamination": "Yes",
      "contaminant": "microalgae",
      "qualityScoring": 5,
      "developmentalStage": "Juvenile Sporophyte Growth",
      "biologicalSexRatio": "60/40",
      "comment": None
    },
    {
      "date": "2026-01-20T09:45:00Z",
      "technician": "Reiss Jones",
      "contamination": "No",
      "contaminant": None,
      "qualityScoring": 8,
      "developmentalStage": "Spore Release",
      "biologicalSexRatio": "40/60",
      "comment": None
    }
  ]
}

def seed_db():
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()
        print("Database tables re-created.")

        # Seed Batches
        batch_map = {} # string_id -> int_id
        for b in BATCHES:
            batch = Batch(
                code=b['id'],
                name=b['batchName'],
                batch_date=b['batchDate']
            )
            db.session.add(batch)
            db.session.flush() # Get the auto-incremented ID
            batch_map[b['id']] = batch.id
            
        print(f"Seeded {len(BATCHES)} batches.")

        # Seed QC Records
        count = 0
        for old_batch_id, records in QC_RECORDS.items():
            new_batch_id = batch_map.get(old_batch_id)
            if not new_batch_id: continue
            
            for r in records:
                qc_record = QCRecord(
                    batch_id=new_batch_id,
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
        print(f"Seeded {count} QC records.")

        db.session.commit()
        print("Seeding complete.")

if __name__ == '__main__':
    seed_db()
