class SonarEnv {
    constructor(map_size = 200, spawn_padding = 50, max_theta, max_velocity, motor_pwm_values = []) {
        this.map_size = map_size || 200;
        this.spawn_padding = spawn_padding || 50;
        this.motor_input_values = motor_input_values || this._generate_random_motor_input();
        this.position = this._generate_random_spawn_position();
        this.velocity = [];
        this.theta = this.generate_random_theta();
        this.max_theta = max_theta;
        this.max_velocity = max_velocity;
    }

    _generate_random_motor_input() {
        // throttle roll pitch yaw
        let motor_inputs = [];
        for(let i = 0; i < 4; i++) motor_inputs.push(Math.random() * 0.5 + 0.25)
        return motor_inputs;
    }

    _generate_random_theta() {
        let thetas = [];
        for(let i = 0; i < 3; i++) {
            thetas.push(((Math.random() * 2) - 1) * this.max_theta);
        }
        return thetas;
    }

    _generate_random_spawn_position() {
        let position = [];
        for(let i = 0; i < 3; i++) position.push(Math.random() * (this.map_size - 2 * this.spawn_padding) + this.spawn_padding)
        return position;
    }

    _get_sonar() {
        return [
            this.position[2],
            this.map_size - this.position[2],
            this.position[0],
            this.map_size - this.position[0],
            this.position[1],
            this.map_size - this.position[1]
        ]
    }

    _get_reward() {
        let distance_reward_vecs = [];
        for(let i of this.position) {
            distance_reward_vecs.push(
                Math.pow(1 - (((this.map_size / 2) % i) || 0.01) / (this.map_size / 2), 2)
            )
        }
        return distance_reward_vecs.reduce((a, b) => a + b) / this.position.length;
    }

    _is_done() {
        for(let i of this.position) if(i > this.map_size || i < 0) return true;
        return false;
    }

    reset() {
        this.motor_input_values = this._generate_random_motor_input();
        this.position = this._generate_random_spawn_position();
        this.theta = this._generate_random_theta();
    }

    step(action) {
        if(!(action.length == 4)) throw new Error("Need 4 float inputs");
        this.motor_input_values = action;
        this.theta[0] = (this.motor_input_values[1] - 0.5) * this.max_theta * 2;
        this.theta[1] = (this.motor_input_values[2] - 0.5) * this.max_theta * 2;
        thrust_level = (this.motor_input_values[0] * this.max_velocity)
        this.velocity[0] += thrust_level * Math.cos(this.theta[0]);
        this.velocity[1] += thrust_level - 9.8;
        this.velocity[3] += thrust_level * Math.cos(this.theta[1]);
        this.position[0] += this.velocity[0];
        this.position[1] += this.velocity[1];
        this.position[2] += this.velocity[2];
        return [this._get_sonar(), this._get_reward(), this._is_done()];
    }

    get_observation() {
        return [this._get_sonar(), this._get_reward(), this._is_done()];
    }
}

const EnvCommandMap = env => (command, params) => {
    switch(command) {
        case "reset":
            return env.reset();
        case "step":
            return env.step(params);
        case "get_observation":
            return env.get_observation();
        default: return null;
    }
}

module.exports = {
    SonarEnv,
    EnvCommandMap
}