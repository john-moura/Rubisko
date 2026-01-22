import { Link } from 'react-router-dom'
import { formatLocalDate } from '../utils/dateUtils'
import './BatchCard.css'

interface BatchCardProps {
    batchId: number
    batchName: string
    batchDate: string
}

const BatchCard = ({ batchId, batchName, batchDate }: BatchCardProps) => {
    return (
        <Link to={`/batch/${batchId}`} className="batch-card">
            <div className="batch-card-icon">🌿</div>
            <div className="batch-card-info">
                <h3 className="batch-card-title">{batchName}</h3>
                <p className="batch-card-date">{formatLocalDate(batchDate)}</p>
            </div>
        </Link>
    )
}

export default BatchCard
