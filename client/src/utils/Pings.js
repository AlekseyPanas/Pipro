import { pingData } from "./testData";
import { updatePingCoordinates } from "./utils";
const SCALING_CONSTANT = 20;

class Pings {
  constructor(id, location, active) {
    this.id = id;
    this.location = location;
    this.active = active;
  }

  id = () => {
    return this.id;
  };
  location = () => {
    return this.location;
  };
  active = () => {
    return this.active;
  };

  updatePing = (mouseX, mouseY) => {
    let d = this.dist(mouseX, mouseY, this.location[0], this.location[1]);
    if (d <= 30) {
      let data = updatePingCoordinates(this.id);
      return true
    }
    return false
  };

  dist = (x1, y1, x2, y2) => {
    x2 = x2 * SCALING_CONSTANT
    y2 = y2 * SCALING_CONSTANT
    var a = x1 - x2;
    var b = y1 - y2;
    console.log(x1, y1);
    console.log(x2, y2);
    console.log(Math.sqrt(a * a + b * b));
    return Math.sqrt(a * a + b * b);
  };
}

export default Pings;
