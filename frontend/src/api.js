// src/api.js
const BASE_URL = 'http://localhost:8000/api'; // замени на свой URL

export async function getPosts() {
  const response = await fetch(`${BASE_URL}/posts/`);
  if (!response.ok) throw new Error('Ошибка при загрузке постов');
  return await response.json();
}

export async function createPost(data) {
  const response = await fetch(`${BASE_URL}/posts/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      // 'Authorization': 'Bearer ...' если JWT
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) throw new Error('Ошибка при создании поста');
  return await response.json();
}
