import { useState, useEffect } from 'react'
import api from '../api/axios'

export default function Articles() {
  const [articles, setArticles] = useState([])

  useEffect(() => {
    api.get('/articles/')
      .then(res => setArticles(res.data))
      .catch(err => console.error(err))
  }, [])

  return (
    <div>
      <h1>Новости</h1>
      {articles.map(article => (
        <div key={article.id}>
          <h2>{article.title}</h2>
          <p>{article.text}</p>
          <small>Автор: {article.author_name}</small>
        </div>
      ))}
    </div>
  )
}
