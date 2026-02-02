import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Articles from './pages/Articles'
import ArticleDetail from './pages/ArticleDetail'  // Импортируем компонент для детальной статьи
import Login from './pages/Login'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Articles />} />
        <Route path="/login" element={<Login />} />
        <Route path="/article/:id" element={<ArticleDetail />} />  {/* Этот маршрут для детальной статьи */}
      </Routes>
    </BrowserRouter>
  )
}
