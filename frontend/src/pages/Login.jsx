import { useState } from 'react'
import api from '../api/axios'
import { Link } from 'react-router-dom'

export default function Login() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      const res = await api.post('/token/', {
        username,
        password
      })

      localStorage.setItem('access', res.data.access)
      localStorage.setItem('refresh', res.data.refresh)

      alert('Успешный вход!')
    } catch {
      setError('Неверный логин или пароль')
    }
  }

  return (
    <div>
      <button>
      <Link to="/">На главную</Link>
      </button>


    <form onSubmit={handleSubmit}>
      <h2>Вход</h2>

      <input
        placeholder="Логин"
        value={username}
        onChange={e => setUsername(e.target.value)}
      />

      <input
        type="password"
        placeholder="Пароль"
        value={password}
        onChange={e => setPassword(e.target.value)}
      />

      <button type="submit">Войти</button>

      {error && <p style={{color: 'red'}}>{error}</p>}
    </form>
    </div>
    
  )
}
