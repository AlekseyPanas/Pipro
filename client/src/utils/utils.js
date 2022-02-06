import axios from "axios";
import { pingData, wallData, pipeData } from "./testData";
import Pings from "./Pings";


const pingCoordinates = async () => {
  let pingArray = [];
  // GET request here
  axios
    .get("http://127.0.0.1:5000/data", {
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
    })
    .then((response) => {
      console.log(response);
    });

  // CREATES PING OBJECT AND ADDS TO ARRAY
  for (let i = 0; i < pingData.ping.length; i++) {
    let id = pingData.ping[i].id;
    let location = pingData.ping[i].location;
    let active = pingData.ping[i].active;
    let ping = new Pings(id, location, active);
    pingArray.push(ping);
  }
  console.log(pingArray);
  return pingArray;
};

const wallCoordinates = async () => {
  let testing = await axios.get("https://opentdb.com/api.php?amount=10");
  return wallData;
};

const pipeCoordinates = async () => {
  let pipeArray = []
  return pipeData
}

const updatePingCoordinates = (pingId) => {
  let pingIndex = pingData.ping.findIndex((ping) => ping.id == pingId);
  console.log(pingIndex);
  // SEND POST REQUEST HERE
  pingData.ping[pingIndex].active = false;
  // Send POST request here
  console.log("changed");
};

export {
  pingCoordinates,
  wallCoordinates,
  updatePingCoordinates,
  pipeCoordinates,
};
