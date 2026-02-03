import { useState } from 'react'
import api from '../api/axios'
import { useNavigate } from 'react-router-dom'

export default function CreateArticle() {
  const [title, setTitle] = useState('')
  const [text, setText] = useState('')
  const [category, setCategory] = useState('')
  const [error, setError] = useState('')
  const [success, setSuccess] = useState(false)
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()

    // Получаем токен из localStorage и извлекаем ID пользователя
    const userId = localStorage.getItem('userId')  // ID пользователя, который залогинен

    // Если токен есть, добавляем ID пользователя в запрос
    const articleData = {
      title,
      text,
      category,
      user: userId,  // Добавляем ID пользователя в данные статьи
    }

    console.log('Данные для отправки на сервер:', articleData)  // Логируем данные

    try {
      const res = await api.post('/articles/', articleData)
      setSuccess(true)
      setError('')
      navigate('/articles')  // Перенаправляем на страницу с статьями
    } catch (err) {
      console.error('Ошибка при создании статьи:', err)
      setError('Ошибка при создании статьи')
      setSuccess(false)
    }
  }

  return (
    <div>
      <h1>Создать статью</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Заголовок</label>
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
          />
        </div>

        <div>
          <label>Текст</label>
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            required
          />
        </div>

        <div>
          <label>Категория</label>
          <select
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            required
          >
            <option value="technology">Технологии</option>
            <option value="science">Наука</option>
            <option value="sport">Спорт</option>
            <option value="art">Искусство</option>
            <option value="education">Образование</option>
            <option value="other">Другое</option>
          </select>
        </div>

        <button type="submit">Создать статью</button>
      </form>

      {success && <p>Статья успешно создана!</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  )
}
