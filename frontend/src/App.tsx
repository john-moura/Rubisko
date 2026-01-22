import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Home from './pages/Home'
import QualityControl from './pages/QualityControl'
import BatchDetail from './pages/BatchDetail'
import './App.css'

function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/quality-control" element={<QualityControl />} />
          <Route path="/batch/:batchId" element={<BatchDetail />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  )
}

export default App
