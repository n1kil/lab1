import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import api from '../api/axios'

export default function ArticleDetail() {
  const { id } = useParams()  
  const [article, setArticle] = useState(null)
  const [comments, setComments] = useState([])  

 useEffect(() => {
  api.get(`/articles/${id}/`)
    .then(res => setArticle(res.data))
    .catch(err => console.error('Ошибка при получении статьи:', err))

  api.get(`/comment/?article=${id}`)
    .then(res => {
      console.log('Комментарии получены:', res.data);  
      setComments(res.data);
    })
    .catch(err => console.error('Ошибка при получении комментариев:', err))
}, [id])


  if (!article) return <p>Загрузка...</p>

  const createdDate = new Date(article.created_date)

  return (
    <div>
      <h1>{article.title}</h1>
      <p>{article.text}</p>
      <small>Автор: {article.author_name}</small>
      <p>Категория: {article.category}</p>
      <p>Дата создания: {createdDate.toLocaleString()}</p>

      
      <button>
        <Link to="/">На главную</Link>
      </button>

      <h3>Комментарии</h3>
      {comments.length === 0 ? (
        <p>Нет комментариев.</p>
      ) : (
        comments.map(comment => (
          <div key={comment.id} className="comment">
            <h4>{comment.author_name}</h4>
            <p>{comment.text}</p>
            <small>Дата: {new Date(comment.date).toLocaleString()}</small>
          </div>
        ))
      )}
    </div>
  )
}
