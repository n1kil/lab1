import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import api from '../api/axios'
import './Articles.css'

export default function Articles() {
  const [articles, setArticles] = useState([])
  const [categories, setCategories] = useState([])  
  const [selectedCategory, setSelectedCategory] = useState('')  

  useEffect(() => {
    api.get('/articles/')
      .then(res => {
        setArticles(res.data)

        const uniqueCategories = Array.from(new Set(res.data.map(article => article.category)))
        setCategories(uniqueCategories)
      })
      .catch(err => console.error('Ошибка при получении статей:', err))
  }, [])

  const filteredArticles = selectedCategory
    ? articles.filter(article => article.category === selectedCategory)
    : articles

  return (
    <div>
      <button>
        <Link to="/">На главную</Link>
      </button>

      <h1>Новости</h1>
      <select onChange={e => setSelectedCategory(e.target.value)} value={selectedCategory}>
        <option value="">Все категории</option>
        {categories.map((category, index) => (
          <option key={index} value={category}>
            {category}
          </option>
        ))}
      </select>

      {filteredArticles.length === 0 ? (
        <p>Загрузка...</p>
      ) : (
        filteredArticles.map(article => (
          <div key={article.id} className="article-card">
            <Link to={`/article/${article.id}`}>
              <h2>{article.title}</h2>
            </Link>
            <p>{article.text}</p>
            <small>Автор: {article.author_name}</small>
            <p className="article-date">Дата создания: {new Date(article.created_date).toLocaleString()}</p>
            <p className="article-category">Категория: {article.category}</p> 
          </div>
        ))
      )}
    </div>
  )
}
