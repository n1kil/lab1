import { useEffect, useState } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import api from '../api/axios';

export default function ArticleDetail() {
  const { id } = useParams();
  const [article, setArticle] = useState(null);
  const [comments, setComments] = useState([]);
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({ title: '', text: '' });
  
  // Отдельные состояния для создания нового комментария
  const [newCommentText, setNewCommentText] = useState('');
  const [newAuthorName, setNewAuthorName] = useState('');
  
  // Отдельные состояния для редактирования комментария
  const [editCommentId, setEditCommentId] = useState(null);
  const [editCommentText, setEditCommentText] = useState('');
  const [editAuthorName, setEditAuthorName] = useState('');
  
  const navigate = useNavigate();

  // Функция для загрузки комментариев
  const loadComments = () => {
    api.get(`/comment/?article=${id}`)
      .then(res => setComments(res.data))
      .catch(err => console.error('Ошибка при получении комментариев:', err));
  };

  useEffect(() => {
    api.get(`/articles/${id}/`)
      .then(res => {
        setArticle(res.data);
        setFormData({ title: res.data.title, text: res.data.text });
      })
      .catch(err => console.error('Ошибка при получении статьи:', err));

    loadComments();
  }, [id]);

  const handleDelete = async () => {
    try {
      await api.delete(`/articles/${id}/`);
      alert('Статья удалена!');
      navigate('/articles');
    } catch (err) {
      console.error('Ошибка при удалении статьи:', err);
      alert('Не удалось удалить статью.');
    }
  };

  const handleEdit = () => {
    setIsEditing(true);
  };

  const handleFormChange = (e) => {
    const { name, value } = e.target;
    setFormData(prevState => ({
      ...prevState,
      [name]: value
    }));
  };

  const handleSave = async () => {
    try {
      const updatedArticle = {
        title: formData.title,
        text: formData.text,
      };
      const res = await api.put(`/articles/${id}/`, updatedArticle);
      setArticle(res.data);
      setFormData({ title: res.data.title, text: res.data.text });
      setIsEditing(false);
      alert('Статья обновлена!');
    } catch (err) {
      console.error('Ошибка при обновлении статьи:', err);
      alert('Не удалось обновить статью.');
    }
  };

  const handleCreateComment = async () => {
    if (!newAuthorName || !newCommentText) {
      alert('Имя автора и комментарий обязательны для заполнения.');
      return;
    }

    try {
      const newComment = { 
        text: newCommentText, 
        author_name: newAuthorName, 
        article: id 
      };
      await api.post('/comment/', newComment);
      
      // Очищаем поля и обновляем комментарии
      setNewCommentText('');
      setNewAuthorName('');
      loadComments(); // Перезагружаем комментарии
      alert('Комментарий добавлен!');
    } catch (err) {
      console.error('Ошибка при добавлении комментария:', err);
      alert('Не удалось добавить комментарий.');
    }
  };

  const handleEditComment = (commentId, text, authorName) => {
    setEditCommentId(commentId);
    setEditCommentText(text);
    setEditAuthorName(authorName);
    
    // Очищаем поля для нового комментария
    setNewCommentText('');
    setNewAuthorName('');
  };

  const handleUpdateComment = async () => {
    if (!editAuthorName || !editCommentText) {
      alert('Имя автора и комментарий обязательны для заполнения.');
      return;
    }

    try {
      // Вариант 1: Попробуйте отправить данные в таком формате
      const updatedComment = { 
        text: editCommentText, 
        author_name: editAuthorName,
        // Возможно, сервер ожидает поле article
        article: parseInt(id)
      };

      console.log('Отправка данных на обновление комментария:', updatedComment);
      console.log('URL:', `/comment/${editCommentId}/`);
      
      await api.put(`/comment/${editCommentId}/`, updatedComment);
      
      // Сбрасываем состояние редактирования и обновляем комментарии
      setEditCommentId(null);
      setEditCommentText('');
      setEditAuthorName('');
      loadComments(); // Перезагружаем комментарии
      alert('Комментарий обновлён!');
    } catch (err) {
      console.error('Ошибка при обновлении комментария:', err);
      alert(`Не удалось обновить комментарий: ${err.response ? err.response.data : 'Неизвестная ошибка'}`);
    }
  };

  const handleCancelEdit = () => {
    setEditCommentId(null);
    setEditCommentText('');
    setEditAuthorName('');
  };

  const handleDeleteComment = async (commentId) => {
    try {
      await api.delete(`/comment/${commentId}/`);
      loadComments(); // Перезагружаем комментарии
      alert('Комментарий удалён!');
    } catch (err) {
      console.error('Ошибка при удалении комментария:', err);
      alert('Не удалось удалить комментарий.');
    }
  };

  if (!article) return <p>Загрузка...</p>;

  const createdDate = new Date(article.created_date);

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

      <button onClick={handleEdit}>Редактировать</button>
      <button onClick={handleDelete}>Удалить</button>

      {isEditing && (
        <div>
          <h3>Редактировать статью</h3>
          <form onSubmit={e => e.preventDefault()}>
            <div>
              <label>Заголовок:</label>
              <input
                type="text"
                name="title"
                value={formData.title}
                onChange={handleFormChange}
              />
            </div>
            <div>
              <label>Текст статьи:</label>
              <textarea
                name="text"
                value={formData.text}
                onChange={handleFormChange}
              />
            </div>
            <button type="button" onClick={handleSave}>Сохранить</button>
          </form>
        </div>
      )}

      <h3>Комментарии</h3>

      {/* Форма для создания нового комментария */}
      <div>
        <h4>{editCommentId ? 'Редактировать комментарий' : 'Добавить комментарий'}</h4>
        
        {!editCommentId ? (
          // Форма создания нового комментария
          <>
            <input
              type="text"
              value={newAuthorName}
              onChange={(e) => setNewAuthorName(e.target.value)}
              placeholder="Имя автора"
            />
            <p></p>
            <textarea
              value={newCommentText}
              onChange={(e) => setNewCommentText(e.target.value)}
              placeholder="Оставьте комментарий"
            />
            <p></p>
            <button onClick={handleCreateComment}>Добавить комментарий</button>
          </>
        ) : (
          // Форма редактирования существующего комментария
          <>
            <input
              type="text"
              value={editAuthorName}
              onChange={(e) => setEditAuthorName(e.target.value)}
              placeholder="Имя автора"
            />
            <p></p>
            <textarea
              value={editCommentText}
              onChange={(e) => setEditCommentText(e.target.value)}
              placeholder="Отредактируйте комментарий"
            />
            <p></p>
            <button onClick={handleUpdateComment}>Сохранить изменения</button>
            <button onClick={handleCancelEdit}>Отмена</button>
          </>
        )}
      </div>

      {comments.length === 0 ? (
        <p>Нет комментариев.</p>
      ) : (
        comments.map(comment => (
          <div key={comment.id} className="comment">
            <h4>{comment.author_name}</h4>
            <p>{comment.text}</p>
            <small>Дата: {new Date(comment.date).toLocaleString()}</small>
            <button onClick={() => handleEditComment(comment.id, comment.text, comment.author_name)}>
              Редактировать
            </button>
            <button onClick={() => handleDeleteComment(comment.id)}>
              Удалить
            </button>
          </div>
        ))
      )}
    </div>
  );
}