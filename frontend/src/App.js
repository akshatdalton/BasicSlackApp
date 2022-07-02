import { useState } from 'react';
import './App.css';
import axios from "axios";

function App() {
  const ngrok_url = "https://409e-2401-4900-1c36-13c-2914-c013-862d-7427.in.ngrok.io";

  const [email, setEmail] = useState("");
  const [accountId, setAccountId] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
        const res = await axios.post(`${ngrok_url}/login`, {
            email
        });
        if (res.status === 200) {
            setAccountId(res.data.account_id);
            localStorage.setItem("token", res.data.token);
            setEmail("");
        } else {
            console.error(`Error: ${res.status}`);
        }
    } catch (err) {
        console.error(`Error: ${err}`);
    }
  };

    return (
      <>
        <h4>
          Account ID:
        {accountId}
        </h4>
        <form onSubmit={handleSubmit}>
          <label>
            Email:
            <input type="text" onChange={(e) => setEmail(e.target.value)} value={email || ""} />
          </label>
          <input type="submit" value="Login" />
        </form>
        <br/>
        {accountId ?
          <a href={ngrok_url + "/start_auth_flow/" + accountId}>
            <img alt="Add to Slack" height="40" width="139" src="https://platform.slack-edge.com/img/add_to_slack.png" srcSet="https://platform.slack-edge.com/img/add_to_slack.png 1x, https://platform.slack-edge.com/img/add_to_slack@2x.png 2x" />
          </a>
        : <></>
        }
      </>
    );
}

export default App;
