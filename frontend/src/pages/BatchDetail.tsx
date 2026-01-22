import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { formatLocalDate } from '../utils/dateUtils'
import { API_BASE_URL } from '../apiConfig'
import './BatchDetail.css'

interface BatchDetail {
    id: number
    batchName: string
    batchDate: string
}

interface QCRecord {
    id: number
    date: string
    technician: string
    contamination: string
    contaminant: string | null
    qualityScoring: number
    developmentalStage: string
    biologicalSexRatio: string
    comment?: string
    imageUrl?: string
}

const BatchDetail = () => {
    const { batchId } = useParams<{ batchId: string }>()
    const [batchDetail, setBatchDetail] = useState<BatchDetail | null>(null)
    const [qcRecords, setQcRecords] = useState<QCRecord[]>([])
    const [loading, setLoading] = useState(true)
    const [uploading, setUploading] = useState(false)
    const [uploadMessage, setUploadMessage] = useState('')
    const [selectedRecord, setSelectedRecord] = useState<QCRecord | null>(null)
    const [isEditing, setIsEditing] = useState(false)
    const [editedRecord, setEditedRecord] = useState<QCRecord | null>(null)

    useEffect(() => {
        if (!batchId) return

        const fetchData = async () => {
            try {
                const [batchRes, qcRes] = await Promise.all([
                    fetch(`${API_BASE_URL}/api/batch/${batchId}`),
                    fetch(`${API_BASE_URL}/api/batch/${batchId}/qc-records`)
                ])

                const batchData = await batchRes.json()
                const qcData = await qcRes.json()

                if (batchData.error) {
                    setBatchDetail(null)
                } else {
                    setBatchDetail(batchData)
                }
                setQcRecords(qcData)
            } catch (err) {
                console.error('Error fetching data:', err)
            } finally {
                setLoading(false)
            }
        }

        fetchData()
    }, [batchId])

    const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files?.[0]
        if (!file) return

        // Check file type
        const validTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp', 'video/mp4', 'video/webm', 'video/mov', 'video/quicktime']
        console.log(file.type)
        if (!validTypes.includes(file.type)) {
            setUploadMessage('Please upload an image or video file')
            return
        }

        setUploading(true)
        setUploadMessage('Analyzing data...')

        try {
            const formData = new FormData()
            formData.append('file', file)
            formData.append('batchId', batchId || '')

            const response = await fetch(`${API_BASE_URL}/api/analyze-qc-image`, {
                method: 'POST',
                body: formData
            })

            const data = await response.json()

            if (data.success && data.analysis) {
                // Add new record to the beginning of the table
                setQcRecords([data.analysis, ...qcRecords])
                setUploadMessage('Analysis complete! New record added to table.')

                // Clear message after 3 seconds
                setTimeout(() => setUploadMessage(''), 3000)
            } else {
                setUploadMessage(`Error: ${data.error || 'Analysis failed'}`)
            }
        } catch (error) {
            setUploadMessage(`Error: ${error instanceof Error ? error.message : 'Upload failed'}`)
        } finally {
            setUploading(false)
            // Reset file input
            event.target.value = ''
        }
    }

    const handleSaveEdit = async () => {
        if (!editedRecord) return

        try {
            const response = await fetch(`${API_BASE_URL}/api/qc-record/${editedRecord.id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(editedRecord)
            })

            const data = await response.json()

            if (data.success) {
                // Update local records
                setQcRecords(qcRecords.map(r => r.id === editedRecord.id ? data.record : r))
                setSelectedRecord(data.record)
                setIsEditing(false)
                setUploadMessage('Changes saved successfully!')
                setTimeout(() => setUploadMessage(''), 3000)
            } else {
                alert(`Error: ${data.error}`)
            }
        } catch (error) {
            console.error('Error saving record:', error)
            alert('Failed to save changes.')
        }
    }

    const startEditing = () => {
        setEditedRecord(selectedRecord)
        setIsEditing(true)
    }

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
        if (!editedRecord) return
        const { name, value } = e.target
        setEditedRecord({ ...editedRecord, [name]: value })
    }

    if (loading) {
        return <div className="batch-detail-page">Loading...</div>
    }

    if (!batchDetail) {
        return (
            <div className="batch-detail-page">
                <h1>Batch Not Found</h1>
                <p>The requested batch could not be found.</p>
            </div>
        )
    }

    return (
        <div className="batch-detail-page">
            <h1 className="page-title">Batch Details</h1>

            {/* Batch Info Table */}
            <div className="batch-table-container">
                <table className="batch-table">
                    <thead>
                        <tr>
                            <th>Batch name</th>
                            <th>Batch date</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>{batchDetail.batchName}</td>
                            <td>{formatLocalDate(batchDetail.batchDate)}</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            {/* Quality Control Records Section */}
            <div className="qc-header">
                <h2 className="section-title">Quality Control Records</h2>
                <div className="upload-section">
                    <label htmlFor="file-upload" className={`upload-button ${uploading ? 'uploading' : ''}`}>
                        {uploading ? (
                            <div className="spinner"></div>
                        ) : (
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                                <polyline points="17 8 12 3 7 8"></polyline>
                                <line x1="12" y1="3" x2="12" y2="15"></line>
                            </svg>
                        )}
                        {uploading ? 'Analyzing...' : 'Upload Video/Photo'}
                    </label>
                    <input
                        id="file-upload"
                        type="file"
                        accept="image/*,video/*"
                        onChange={handleFileUpload}
                        disabled={uploading}
                        className="file-input"
                    />
                </div>
            </div>

            {uploadMessage && (
                <div className={`upload-message ${uploading ? 'analyzing' :
                    uploadMessage.includes('Error') ? 'error' : 'success'
                    }`}>
                    {uploadMessage}
                </div>
            )}

            <div className="batch-table-container">
                <table className="batch-table qc-table">
                    <thead>
                        <tr>
                            <th>Date</th>
                            <th>Technician</th>
                            <th>Contamination</th>
                            <th>Contaminant</th>
                            <th>Score</th>
                            <th>Developmental stage</th>
                            <th>Sex ratio (M/F)</th>
                            <th>Comment</th>
                        </tr>
                    </thead>
                    <tbody>
                        {qcRecords.map((record, index) => (
                            <tr
                                key={index}
                                className="clickable-row"
                                onClick={() => setSelectedRecord(record)}
                                title="Click to view details"
                            >
                                <td>{formatLocalDate(record.date)}</td>
                                <td>{record.technician}</td>
                                <td className={record.contamination === 'Yes' ? 'contamination-yes' : ''}>
                                    {record.contamination}
                                </td>
                                <td>{record.contaminant || '-'}</td>
                                <td>{record.qualityScoring}</td>
                                <td>{record.developmentalStage}</td>
                                <td>{record.biologicalSexRatio || '-'}</td>
                                <td className="comment-cell">
                                    {record.comment || '-'}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            {/* Comment Detail Modal */}
            {selectedRecord && (
                <div className="modal-overlay" onClick={() => { setSelectedRecord(null); setIsEditing(false); }}>
                    <div className="modal-content" onClick={(e) => e.stopPropagation()}>
                        <div className="modal-header">
                            <h3>{isEditing ? 'Edit Analysis' : 'Analysis Details'}</h3>
                            <div className="modal-header-actions">
                                {!isEditing && (
                                    <button className="edit-button" onClick={startEditing}>Edit</button>
                                )}
                                <button className="close-button" onClick={() => { setSelectedRecord(null); setIsEditing(false); }}>&times;</button>
                            </div>
                        </div>
                        <div className="modal-body">
                            <div className="modal-image-container">
                                {selectedRecord.imageUrl ? (
                                    selectedRecord.imageUrl.match(/\.(mp4|webm|mov)$/) ? (
                                        <video src={selectedRecord.imageUrl} controls className="modal-media" />
                                    ) : (
                                        <img src={selectedRecord.imageUrl} alt="Sample" className="modal-media" />
                                    )
                                ) : (
                                    <div className="no-image">No image available</div>
                                )}
                            </div>
                            <div className="modal-info">
                                <div className="info-group">
                                    <label>Biologist Comment:</label>
                                    {isEditing ? (
                                        <textarea
                                            name="comment"
                                            value={editedRecord?.comment || ''}
                                            onChange={handleInputChange}
                                            rows={4}
                                            className="edit-input"
                                        />
                                    ) : (
                                        <p>{selectedRecord.comment || 'No comment provided.'}</p>
                                    )}
                                </div>
                                <div className="info-grid">
                                    <div className="info-item">
                                        <label>Technician:</label>
                                        {isEditing ? (
                                            <input name="technician" value={editedRecord?.technician || ''} onChange={handleInputChange} className="edit-input" />
                                        ) : (
                                            <span>{selectedRecord.technician}</span>
                                        )}
                                    </div>
                                    <div className="info-item">
                                        <label>Date:</label>
                                        <span>{formatLocalDate(selectedRecord.date)}</span>
                                    </div>
                                    <div className="info-item">
                                        <label>Scoring (0-10):</label>
                                        {isEditing ? (
                                            <input type="number" name="qualityScoring" min="0" max="10" value={editedRecord?.qualityScoring || 0} onChange={handleInputChange} className="edit-input" />
                                        ) : (
                                            <span>{selectedRecord.qualityScoring}/10</span>
                                        )}
                                    </div>
                                    <div className="info-item">
                                        <label>Contamination:</label>
                                        {isEditing ? (
                                            <select name="contamination" value={editedRecord?.contamination || 'No'} onChange={handleInputChange} className="edit-input">
                                                <option value="No">No</option>
                                                <option value="Yes">Yes</option>
                                            </select>
                                        ) : (
                                            <span className={selectedRecord.contamination === 'Yes' ? 'text-error' : ''}>
                                                {selectedRecord.contamination}
                                            </span>
                                        )}
                                    </div>
                                    <div className="info-item">
                                        <label>Contaminant:</label>
                                        {isEditing ? (
                                            <input name="contaminant" value={editedRecord?.contaminant || ''} onChange={handleInputChange} className="edit-input" placeholder="e.g. bacteria" />
                                        ) : (
                                            <span>{selectedRecord.contaminant || '-'}</span>
                                        )}
                                    </div>
                                    <div className="info-item">
                                        <label>Dev Stage:</label>
                                        {isEditing ? (
                                            <select name="developmentalStage" value={editedRecord?.developmentalStage || ''} onChange={handleInputChange} className="edit-input">
                                                <option value="Spore Release">Spore Release</option>
                                                <option value="Germination">Germination</option>
                                                <option value="Zygote Formation">Zygote Formation</option>
                                                <option value="Juvenile Sporophyte Growth">Juvenile Sporophyte Growth</option>
                                                <option value="Inconclusive">Inconclusive</option>
                                            </select>
                                        ) : (
                                            <span>{selectedRecord.developmentalStage}</span>
                                        )}
                                    </div>
                                    <div className="info-item">
                                        <label>Sex Ratio:</label>
                                        {isEditing ? (
                                            <input name="biologicalSexRatio" value={editedRecord?.biologicalSexRatio || ''} onChange={handleInputChange} className="edit-input" />
                                        ) : (
                                            <span>{selectedRecord.biologicalSexRatio || '-'}</span>
                                        )}
                                    </div>
                                </div>
                                {isEditing && (
                                    <div className="edit-actions">
                                        <button className="cancel-button" onClick={() => setIsEditing(false)}>Cancel</button>
                                        <button className="save-button" onClick={handleSaveEdit}>Save Changes</button>
                                    </div>
                                )}
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    )
}

export default BatchDetail
