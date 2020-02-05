exports = class Sonar {
    constructor(bound) {
        this.bound = bound
        this.motor_values = undefined;
        this.position = undefined;
        this.velocity = undefined;
        this.acceleration = undefined;
        this.bodyOrientation = {x: 0, y: 0, z: 0};
        this.yaw = 0;
    }

    setPosition(position) {
        this._checkVector(position);
        this.position = position;
        return this;
    }

    setVelocity(velocity) {
        this._checkVector(velocity);
        this.velocity = velocity;
        return this;
    }

    setAcceleration(acceleration) {
        this._checkVector(acceleration);
        this.acceleration = acceleration;
        return this;
    }

    step() {
        this._updateX()
        this._updateY()
        this._updateZ()
    }

    _updateX() {
        if(this.position.x <= this.bound && this.position.x >= -this.bound) {
            
        }
    }

    _updateY() {
        if(this.position.y <= this.bound && this.position.y >= -this.bound) {

        }
    }

    _updateZ() {
        if(this.position.z <= this.bound && this.position.z >= -this.bound) {

        }
    }

    _dtr(deg) {
        return deg * (Math.PI / 180);
    }

    _checkVector(v) {
        if(!(typeof v.x == "number" && typeof v.y == "number" && typeof v.z == "number")) 
            throw new Error("Vector should be { x: number, y: number, z:number }")
    }
}