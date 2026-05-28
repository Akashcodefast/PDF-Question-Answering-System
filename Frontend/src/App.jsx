import { useState } from 'react'
import './App.css'
import axios from 'axios'

function App() {
  const [file, setfile] = useState(null)
  const [question, setquestion] = useState("")
  const [answer, setanswer] = useState("")
  const [loading, setloading] = useState(false)

  const handleUpload = async () => {
    if (!file) {
      alert("please Select a PDF file to Upload")
      return
    }
    const formdata = new FormData()
    formdata.append("file", file)
    setloading(true)
    try {
      await axios.post("http://127.0.0.1:5000/upload", formdata)
      alert("File Uploaded Successfully")
    }
    catch (error) {
      console.log(error)
      alert("Error uploading file")
    }
    setloading(false)

  }

  const handleQuestion = async () => {
    if (!question) {
      alert("Please enter a question")
      return
    }
    setloading(true)
    try {
      const response = await axios.post("http://127.0.0.1:5000/ask", { question })
      setanswer(response.data.answer)
    }
    catch (error) {

      console.log(error)
      alert("Error in getting the answer")
    }
    setloading(false)

  }


  return (
    <>
      <div className="container">
        <h1 className="title">PDF QUESTION ANSWERING SYSTEM</h1>
        <div className="file-input">
          <input type="file" accept="application/pdf" onChange={(e) => setfile(e.target.files[0])} />
        </div>
        <button onClick={handleUpload}>Upload PDF</button>
        <br /><br />

      
      <div className="question-section">
        <input type="text" placeholder="Ask a question..." value={question} onChange={(e) => setquestion(e.target.value)} />
      <button onClick={handleQuestion}>Ask Question</button>
      </div>
      


      {
        loading ? <p>Loading...</p> : null
      }

      {
        answer && <div className="answer-section">
          <h2>Answer:</h2>
          <p>{answer}</p>
          <div className="button-section">
            The Answer will be based on the content of the uploaded PDF file.
          </div>
        </div>

      }
</div>


    </>
  )
}

export default App
