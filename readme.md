# Документация API

## Базовый URL
Все эндпоинты доступны по базовому адресу:  
`http://localhost:8000`

---

## Авторизация

### 1. **POST /login/**  
**Описание:** Авторизация пользователя по email и паролю.

**Тело запроса:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Ответ:**
- **200 OK**
```json
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe"
  }
}
```
- **401 Unauthorized**
```json
{
  "detail": "Incorrect email or password"
}
```

---

### 2. **POST /register/**  
**Описание:** Регистрация нового пользователя.

**Тело запроса:**
```json
{
  "email": "user@example.com",
  "password": "password123",
  "name": "John Doe"
}
```

**Ответ:**
- **200 OK**
```json
{
  "message": "User registered successfully"
}
```
- **400 Bad Request**
```json
{
  "detail": "Email already registered"
}
```

---

## Работа с транзакциями

### 3. **POST /transactions/{user_id}/**  
**Описание:** Добавление новой транзакции для пользователя.  

**Параметры пути:**
- `user_id` (str): Идентификатор пользователя.

**Тело запроса:**
```json
{
  "date": "2024-11-29",
  "type": "income",
  "category": "Salary",
  "place": "Office",
  "amount": 1000.00,
  "description": "Salary for November"
}
```

**Ответ:**
- **200 OK**
```json
{
  "id": 1,
  "date": "2024-11-29",
  "type": "income",
  "category": "Salary",
  "place": "Office",
  "amount": 1000.00,
  "description": "Salary for November"
}
```
- **404 Not Found**
```json
{
  "detail": "User not found"
}
```
- **400 Bad Request**
```json
{
  "detail": "Invalid transaction type"
}
```

---

### 4. **GET /transactions/{user_id}/**  
**Описание:** Получение всех транзакций пользователя.  

**Параметры пути:**
- `user_id` (str): Идентификатор пользователя.

**Ответ:**
- **200 OK**
```json
[
  {
    "id": 1,
    "date": "2024-11-29",
    "type": "income",
    "category": "Salary",
    "place": "Office",
    "amount": 1000.00,
    "description": "Salary for November"
  }
]
```
- **404 Not Found**
```json
{
  "detail": "No transactions found for this user"
}
```

---

### 5. **DELETE /transactions/{user_id}/{transaction_id}/**  
**Описание:** Удаление конкретной транзакции пользователя.  

**Параметры пути:**
- `user_id` (str): Идентификатор пользователя.  
- `transaction_id` (int): Идентификатор транзакции.

**Ответ:**
- **200 OK**
```json
{
  "message": "Transaction deleted successfully"
}
```
- **404 Not Found**
```json
{
  "detail": "Transaction not found"
}
```

---

### 6. **GET /transactions/{user_id}/{start_date}/{end_date}/**  
**Описание:** Получение транзакций за указанный период.  

**Параметры пути:**
- `user_id` (str): Идентификатор пользователя.  
- `start_date` (str): Начальная дата в формате `YYYY-MM-DD`.  
- `end_date` (str): Конечная дата в формате `YYYY-MM-DD`.

**Ответ:**
- **200 OK**
```json
[
  {
    "id": 1,
    "date": "2024-11-29",
    "type": "income",
    "category": "Salary",
    "place": "Office",
    "amount": 1000.00,
    "description": "Salary for November"
  }
]
```
- **404 Not Found**
```json
{
  "detail": "No transactions found for this user"
}
```

---

## Структура данных

### Пользователь (User)
| Поле      | Тип   | Описание                |
|-----------|-------|-------------------------|
| `id`      | int   | Уникальный идентификатор пользователя. |
| `email`   | str   | Email пользователя.     |
| `password`| str   | Пароль пользователя.    |
| `name`    | str   | Имя пользователя.       |

### Транзакция (Transaction)
| Поле         | Тип    | Описание                       |
|--------------|--------|--------------------------------|
| `id`         | int    | Уникальный идентификатор транзакции. |
| `date`       | str    | Дата транзакции в формате `YYYY-MM-DD`. |
| `type`       | str    | Тип транзакции: `income` или `expense`. |
| `category`   | str    | Категория транзакции.          |
| `place`      | str    | Место транзакции.              |
| `amount`     | float  | Сумма транзакции.              |
| `description`| str    | Описание транзакции (необязательное поле). |
