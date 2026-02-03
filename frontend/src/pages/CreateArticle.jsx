import { Link } from 'react-router-dom'
export default function CreateArticle() {
  return (
    <div>
        <button>
            <Link to="/">На главную</Link>
        </button>
      <h1>Создать статью</h1>
      <p>Страница для создания статьи. Пока что она пустая.</p>
    </div>
  )
}
