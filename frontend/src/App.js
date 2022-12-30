import axios from "axios";

function App() {
  const handleLogin = () => {
    const response = axios
      .post("https://127.0.0.1:5000/authentication", {
        id: "test",
        password: "123",
      })
      .then((response) => {
        if (response.status === 200) {
          console.log(response.data.csrf_token);
          localStorage.setItem("csrf_token", response.data.csrf_token);
        }
      });
  };

  const handleGetInfo = () => {
    axios
      .get("https://127.0.0.1:5000/get_info", {
        headers: { csrf_token: localStorage.getItem("csrf_token") },
      })
      .then((res) => {
        alert(res.data);
      })
      .catch((err) => {
        alert(err.response.data.status);
        console.log(err.response);
      });
  };

  return (
    <div className="App">
      <button onClick={handleLogin}> Login </button>
      <br />
      <br />
      <button onClick={handleGetInfo}> Get Info </button>
    </div>
  );
}

export default App;
