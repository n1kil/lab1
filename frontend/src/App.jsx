import { BrowserRouter, Routes, Route } from 'react-router-dom'
import HomePage from './pages/HomePage'  
import Articles from './pages/Articles'
import ArticleDetail from './pages/ArticleDetail'
import Login from './pages/Login'
import Register from './pages/Register'  
import CreateArticle from './pages/CreateArticle'  

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage />} />  
        <Route path="/articles" element={<Articles />} />  
        <Route path="/article/:id" element={<ArticleDetail />} /> 
        <Route path="/login" element={<Login />} />  
        <Route path="/register" element={<Register />} />  
        <Route path="/create-article" element={<CreateArticle />} /> 
      </Routes>
    </BrowserRouter>
  )
}
