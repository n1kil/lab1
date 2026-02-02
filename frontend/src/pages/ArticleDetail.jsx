import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import api from '../api/axios'

export default function ArticleDetail() {
  const { id } = useParams()
  const [article, setArticle] = useState(null)

  useEffect(() => {
    api.get(`/articles/${id}/`)
      .then(res => setArticle(res.data))
      .catch(err => console.error('Ошибка при получении статьи:', err))
  }, [id])

  if (!article) return <p>Загрузка...</p>

  // Преобразуем дату из строки в объект Date
  const createdDate = new Date(article.created_date)

  return (
    <div>
      <h1>{article.title}</h1>
      <p>{article.text}</p>
      <small>Автор: {article.author_name}</small>
      <p>Дата создания: {createdDate.toLocaleString()}</p>  {/* Отображаем дату */}
    </div>
  )
}
