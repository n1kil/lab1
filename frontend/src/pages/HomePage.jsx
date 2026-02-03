import { Link } from 'react-router-dom'

export default function HomePage() {
  const isAuthenticated = localStorage.getItem('access') !== null  

  return (
    <div>
      <h1>Главная страница</h1>

      <div>
        <button>
          <Link to="/">На главную</Link>  
        </button>

        <button>
          <Link to="/articles">Все статьи</Link>  
        </button>

        <button>
          <Link to="/create-article">Создать статью</Link>  
        </button>

        {!isAuthenticated ? (  
          <>
            <button>
              <Link to="/login">Авторизоваться</Link>
            </button>
            <button>
              <Link to="/register">Зарегистрироваться</Link>
            </button>
          </>
        ) : (  
          <button onClick={() => {
            localStorage.removeItem('access')
            localStorage.removeItem('refresh')
            window.location.reload() 
          }}>
            Выйти
          </button>
        )}
      </div>
    </div>
  )
}
