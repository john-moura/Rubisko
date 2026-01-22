import { useState, useEffect } from 'react'
import BatchCard from '../components/BatchCard'
import { API_BASE_URL } from '../apiConfig'
import './QualityControl.css'

interface Batch {
    id: number
    batchName: string
    batchDate: string
}

const QualityControl = () => {
    const [batches, setBatches] = useState<Batch[]>([])
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        fetch(`${API_BASE_URL}/api/batches`)
            .then(res => res.json())
            .then(data => {
                setBatches(data)
                setLoading(false)
            })
            .catch(err => {
                console.error('Error fetching batches:', err)
                setLoading(false)
            })
    }, [])

    if (loading) {
        return <div className="quality-control-page">Loading...</div>
    }

    return (
        <div className="quality-control-page">
            <h1 className="page-title">Quality Control</h1>
            <div className="batch-grid">
                {batches.map((batch) => (
                    <BatchCard
                        key={batch.id}
                        batchId={batch.id}
                        batchName={batch.batchName}
                        batchDate={batch.batchDate}
                    />
                ))}
            </div>
        </div>
    )
}

export default QualityControl
