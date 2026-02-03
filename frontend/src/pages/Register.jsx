import { useState} from 'react'
import api from '../api/axios'
import { Link } from 'react-router-dom'

export default function Register() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [success, setSuccess] = useState(false)

  const handleSubmit = async (e) => {
  e.preventDefault()

  try {
    const res = await api.post('/register/', {
      username,
      password,
    })
    setSuccess(true)
    setError('')
  } catch (err) {
    console.error(err);  
    setError('Ошибка при регистрации');
    setSuccess(false)
  }
}

  return (
    <div>
      <button>
        <Link to="/">На главную</Link>
      </button>
      <h1>Регистрация</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Имя пользователя</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>

        <div>
          <label>Пароль</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>

        <button type="submit">Зарегистрироваться</button>
      </form>

      {success && <p>Регистрация успешна! Теперь вы можете войти.</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  )
}
