import { useEffect, useState } from "react";
import { ReactP5Wrapper } from "react-p5-wrapper";
import {
  pingCoordinates,
  wallCoordinates,
  pipeCoordinates,
} from "../utils/utils";

const WIDTH = 500;
const HEIGHT = 500;
const SCALING_CONSTANT = 20;
const COORDINATE_ADJUST = 247;

const RoomBlueprint = () => {
  const [pingData, setPingData] = useState([]);
  const [wallData, setWallData] = useState([]);
  const [pipeData, setPipeData] = useState([]);
  const [removing, setRemoving] = useState(false);
  const [loading, setLoading] = useState(true);
  let counter = 1;

  useEffect(() => {
    const intervalId = setInterval(() => {
      getPingData();
      getWallCoordinates();
      getPipeCoordinates();
      setRemoving(false);
      setLoading(false);
    }, 5000);
    return () => {
      clearInterval(intervalId);
    };
  }, []);

  const getPingData = async () => {
    // GETS PING DATA FROM UTIL
    let data = await pingCoordinates();
    setPingData(data);
  };

  const getWallCoordinates = async () => {
    // GETS WALL DATA FROM UTIL
    let data = await wallCoordinates();
    setWallData(data);
  };

  const getPipeCoordinates = async () => {
    // GETS PIPE DATA FROM UTIL
    let data = await pipeCoordinates();
    setPipeData(data);
  };

  const generateRoom = (p5) => {
    p5.setup = () => {
      p5.createCanvas(WIDTH, HEIGHT, p5.WEBGL);
    };

    p5.draw = () => {
      p5.background("#000000");
      p5.scale(1, -1);

      for (let i = 0; i < pingData.length; i++) {
        if (pingData[i].active) {
          let xPos = pingData[i].location[0] * SCALING_CONSTANT;
          let yPos = pingData[i].location[1] * SCALING_CONSTANT;
          p5.stroke("red");
          p5.strokeWeight(10);
          p5.point(xPos, yPos);
        }
      }

      for (let j = 0; j < wallData.length; j++) {
        let vert1 = wallData[j].vert1;
        let vert2 = wallData[j].vert2;
        p5.scale(1); // Adding scale transformation
        p5.stroke("white");
        p5.strokeWeight(2); // Resulting strokeweight is 5
        p5.line(
          vert1[0] * SCALING_CONSTANT,
          vert1[1] * SCALING_CONSTANT,
          vert2[0] * SCALING_CONSTANT,
          vert2[1] * SCALING_CONSTANT
        );
      }

      for (let j = 0; j < pipeData.length; j++) {
        let vert1 = pipeData[j].vert1;
        let vert2 = pipeData[j].vert2;
        p5.scale(1); // Adding scale transformation
        p5.stroke("blue");
        p5.strokeWeight(2); // Resulting strokeweight is 5
        p5.line(
          vert1[0] * SCALING_CONSTANT,
          vert1[1] * SCALING_CONSTANT,
          vert2[0] * SCALING_CONSTANT,
          vert2[1] * SCALING_CONSTANT
        );
      }

      p5.push();
      p5.pop();
    };

    p5.mousePressed = () => {
      let success = false;
      for (let i = 0; i < pingData.length; i++) {
        if (!success) {
          success = pingData[i].updatePing(
            p5.mouseX - COORDINATE_ADJUST,
            -(p5.mouseY - COORDINATE_ADJUST)
          );
          setRemoving(true);
        } else {
          break;
        }
      }
      console.log("-------");
    };
  };

  return (
    <div className="h-50">
      <div className="flex bg-black shadow-lg w-full h-screen grid place-items-center">
        {removing ? (
          <div
            class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative"
            role="alert"
          >
            <strong class="font-bold">Restoration in Process! </strong>
            <span class="block sm:inline">Drone restoring pipe leakage.</span>
          </div>
        ) : null}
        {loading ? (
          <div
            class="bg-teal-100 border-t-4 border-teal-500 rounded-b text-teal-900 px-4 py-3 shadow-md h-24"
            role="alert"
          >
            <div class="flex">
              <div class="py-1">
                <svg
                  class="fill-current h-6 w-6 text-teal-500 mr-4"
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 20 20"
                >
                  <path d="M2.93 17.07A10 10 0 1 1 17.07 2.93 10 10 0 0 1 2.93 17.07zm12.73-1.41A8 8 0 1 0 4.34 4.34a8 8 0 0 0 11.32 11.32zM9 11V9h2v6H9v-4zm0-6h2v2H9V5z" />
                </svg>
              </div>
              <div>
                <p class="font-bold">PIPRO ACTIVATED</p>
                <p class="text-sm">
                  Drone currently analyzing area and detecting possible
                  leakages.
                </p>
              </div>
            </div>
          </div>
        ) : null}
        <div className="mr-40">
          <ReactP5Wrapper sketch={generateRoom} />
        </div>
      </div>
    </div>
  );
};

export default RoomBlueprint;
