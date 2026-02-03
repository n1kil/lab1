import { Link } from 'react-router-dom'
export default function Register() {
  return (
    <div>
      <button>
        <Link to="/">На главную</Link>
      </button>
      <h1>Регистрация</h1>
      <p>Страница для регистрации пользователя. Пока что она пустая.</p>
    </div>
  )
}
