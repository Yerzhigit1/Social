import { useState, useEffect } from 'react'
import Profile from "../../assets/profile.jpg"
import "../Home/Home.css"
import Left from "../../Components/LeftSide/Left"
import Middle from "../../Components/MiddleSide/Middle"
import Right from '../../Components/RightSide/Right'
import Nav from '../../Components/Navigation/Nav'
import moment from 'moment'
import axios from 'axios'

const Home = ({ setFriendsProfile }) => {
  const [posts, setPosts] = useState([])
  const [body, setBody] = useState("")
  const [importFile, setImportFile] = useState("")
  const [search, setSearch] = useState("")
  const [following, setFollowing] = useState("")
  const [showMenu, setShowMenu] = useState(false)
  const [images, setImages] = useState(null)

  // Получение постов с API
  useEffect(() => {
    const fetchPosts = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/posts/')
        // Преобразуем данные из бэкенда в формат, который ожидает фронтенд
        const postsWithMoment = response.data.results.map(post => ({
          id: post.id,
          profilepicture: Profile, // Временно используем статичное изображение
          username: post.author.username,
          datetime: moment(post.created_at).fromNow(),
          img: post.image,
          body: post.content,
          like: post.like_count,
          comment: post.comments.length
        }))
        setPosts(postsWithMoment)
      } catch (error) {
        console.error("Ошибка при получении постов:", error)
      }
    }
    fetchPosts()
  }, [])

  // handleSubmit теперь только добавляет пост локально (или можно реализовать POST на сервер)
  const handleSubmit = async (e) => {
    e.preventDefault()

    // Пример добавления поста через API (если реализовано на бэке)
    // const formData = new FormData()
    // formData.append('body', body)
    // if (images) formData.append('img', images)
    // try {
    //   const response = await axios.post('http://localhost:8000/api/posts/', formData)
    //   setPosts(prev => [...prev, response.data])
    // } catch (error) {
    //   console.error("Ошибка при добавлении поста:", error)
    // }

    // Если нет API для добавления, просто добавляем локально (как раньше)
    const id = posts.length ? posts[posts.length - 1].id + 1 : 1
    const username = "Vijay"
    const profilepicture = Profile
    const datetime = moment.utc(new Date()).local().startOf('seconds').fromNow()
    const img = images ? { img: URL.createObjectURL(images) } : null

    const obj = {
      id: id,
      profilepicture: profilepicture,
      username: username,
      datetime: datetime,
      img: img && img.img,
      body: body,
      like: 0,
      comment: 0
    }

    const insert = [...posts, obj]
    setPosts(insert)
    setBody("")
    setImages(null)
  }

  return (
    <div className='interface'>
      <Nav
        search={search}
        setSearch={setSearch}
        showMenu={showMenu}
        setShowMenu={setShowMenu}
      />

      <div className="home">
        <Left />

        <Middle
          handleSubmit={handleSubmit}
          body={body}
          setBody={setBody}
          importFile={importFile}
          setImportFile={setImportFile}
          posts={posts}
          setPosts={setPosts}
          search={search}
          setFriendsProfile={setFriendsProfile}
          images={images}
          setImages={setImages}
        />

        <Right
          showMenu={showMenu}
          setShowMenu={setShowMenu}
          following={following}
          setFollowing={setFollowing}
        />
      </div>
    </div>
  )
}

export default Home