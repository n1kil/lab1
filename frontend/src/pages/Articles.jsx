import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import api from '../api/axios'
import './Articles.css'

export default function Articles() {
  const [articles, setArticles] = useState([])

  useEffect(() => {
    api.get('/articles/')
      .then(res => setArticles(res.data))
      .catch(err => console.error('Ошибка при получении статей:', err))
  }, [])

  return (
    <div>
      <h1>Новости</h1>
      {articles.length === 0 ? (
        <p>Загрузка...</p>
      ) : (
        articles.map(article => (
          <div key={article.id} className="article-card">  {/* Обёртка для каждой статьи */}
            <Link to={`/article/${article.id}`}>
              <h2>{article.title}</h2>
            </Link>
            <p>{article.text}</p>
            <small>Автор: {article.author_name}</small>
            <p className="article-date">Дата создания: {new Date(article.created_date).toLocaleString()}</p>  {/* Дата создания */}
          </div>
        ))
      )}
    </div>
  )
}
