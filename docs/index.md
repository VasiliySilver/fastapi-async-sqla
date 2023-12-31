# FastAPI SQLAlchemy 
---

> Документация по FastAPI + SQLAlchemy с асинхронными сессиями

**FastAPI** - это современный веб-фреймворк для создания веб-приложений с автоматически сгенерированной документацией и встроенной поддержкой валидации данных. **SQLAlchemy** - это библиотека для работы с базами данных в Python, позволяющая создавать асинхронные приложения для взаимодействия с базами данных.

В данном примере мы используем FastAPI для создания RESTful API для управления пользователями в базе данных, а также SQLAlchemy для асинхронного взаимодействия с PostgreSQL базой данных.

## **1. Установка зависимостей**

Для начала убедитесь, что у вас установлены необходимые зависимости, такие как FastAPI, SQLAlchemy и asyncpg (драйвер для PostgreSQL). Вы можете установить их с помощью `pip`:

```bash
pip install fastapi sqlalchemy asyncpg
```

## **2. Создание асинхронного движка SQLAlchemy**

В начале кода мы создаем асинхронный движок SQLAlchemy с использованием `create_async_engine` и указываем URL для подключения к базе данных. В данном случае, мы используем PostgreSQL.

```python
DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"
engine = create_async_engine(DATABASE_URL)
```

## **3. Создание асинхронной сессии**

Следующим шагом мы создаем асинхронную сессию для взаимодействия с базой данных. Мы используем `async_sessionmaker` для создания асинхронной сессии.

```python
async_session = async_sessionmaker(engine, expire_on_commit=False)
```

## **4. Описание модели таблицы "User"**

Мы определяем модель таблицы "User", используя SQLAlchemy. В данном случае, она содержит поля `id`, `name` и `email`.

```python
class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
```

## **5. Создание FastAPI приложения**

Далее мы создаем FastAPI приложение, которое будет служить веб-сервером для обработки HTTP-запросов.

``` python
app = FastAPI()
```

## **6. Обработчики маршрутов**

В приложении FastAPI мы определяем несколько обработчиков маршрутов, которые выполняют различные операции с базой данных. Например, мы имеем обработчики для создания, чтения, обновления и удаления пользователей.

## **7. Создание и обновление пользователя**

Обработчики `create_user` и `update_user` выполняют создание и обновление пользователей в базе данных, используя асинхронные сессии SQLAlchemy. При создании пользователя мы используем `await session.commit()` для сохранения изменений в базе данных, а при обновлении пользователя - `await session.refresh(db_user)` для обновления объекта пользователя после изменений в базе данных.

## **8. Получение списка пользователей и чтение пользователя**

Обработчики `fetch_users` и `read_user` выполняют чтение пользователей из базы данных. Мы используем SQLAlchemy для выполнения SQL-запросов и асинхронные сессии для взаимодействия с базой данных. В случае чтения пользователя, мы также обрабатываем случай, когда пользователя с заданным `user_id` нет в базе данных и возвращаем HTTP-статус 404.

## **9. Удаление пользователя**

Обработчик `delete_user` выполняет удаление пользователя из базы данных. Мы сначала проверяем, существует ли пользователь с заданным `user_id`, и затем удаляем его из базы данных с использованием асинхронных сессий SQLAlchemy.

## **10. Запуск приложения**

Наконец, мы используем `uvicorn` для запуска FastAPI приложения на локальном сервере. Вы можете настроить хост и порт по вашему усмотрению.

``` python
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        reload=True,
        port=8000,
    )
```

Этот код создает RESTful API для управления пользователями в базе данных с использованием FastAPI и асинхронных сессий SQLAlchemy, что позволяет обрабатывать запросы асинхронно и эффективно в многопоточной среде.