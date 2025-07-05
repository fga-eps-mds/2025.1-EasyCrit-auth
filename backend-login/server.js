const express = require('express')
const cors = require('cors')
const fs = require('fs')

const app = express()
app.use(cors())
app.use(express.json())


const usuarios = JSON.parse(fs.readFileSync('usuarios.json'))


app.post('/api/login', (req, res) => {
  console.log('Requisição recebida no /api/login')  

  const { email, senha } = req.body

  const user = usuarios.find(u => u.email === email && u.senha === senha)

  if (user) {
    res.json({ user: user.nome })
  } else {
    res.status(401).json({ error: 'Email ou senha incorretos' })
  }
})

const PORT = 4000
app.listen(PORT, () => {
  console.log(`Servidor rodando na porta ${PORT}`)
})
