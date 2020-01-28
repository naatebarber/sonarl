class PilotMap {
    constructor(init_velocity = {x, y}, spawn_padding = 10, direction = "north", map_size = 150) {
        this.init_velocity = init_velocity;
        this.spawn_padding = spawn_padding;
        this.direction = direction;
        this.map_size = map_size;
        this.env = null;
    }

    generate_env() {
        return {
            x_max: Math.floor(this.map_size / 2),
            x_min: -1 * Math.floor(this.map_size / 2),
            y_max: Math.floor(this.map_size / 2),
            y_min: -1 * Math.floor(this.map_size / 2),
            location: {
                x: (Math.random() * (this.map_size - 2 * this.spawn_padding)) + this.spawn_padding, 
                y: (Math.random() * (this.map_size - 2 * this.spawn_padding)) + this.spawn_padding
            },
            velocity: {
                x: this.init_velocity.x,
                y: this.init_velocity.y
            },
            in_bounds: true
        }
    }

    _in_bounds() {
        return (this.env.location.x > -1 * (this.map_size / 2) && this.env.location.x < (this.map_size / 2))
                && (this.env.location.y > -1 * (this.map_size / 2) && this.env.location.y < (this.map_size / 2))
    }

    _distance_from_center() {
        return Math.sqrt(Math.pow(this.env.location.x, 2) + Math.pow(this.env.location.y, 2))
    }

    observation() {
        return this.env
    }

    step(action) {
        switch(action) {
            case 0: // north
                this.env.velocity.y += 0.2;
                break;
            case 1: // south
                this.env.velocity.y -= 0.2;
                break;
            case 2: // east
                this.env.velocity.x += 0.2;
                break;
            case 3: // west
                this.env.velocity.x -= 0.2
                break;
            default:
                throw new Error("Invalid action, select 0-3")
        }
        this.env.location.x += this.env.velocity.x;
        this.env.location.y += this.env.velocity.y;
        this.env.in_bounds = this._in_bounds();
        if(this.env.in_bounds) 
            return {
                o: this.env,
                r: Math.pow(this._distance_from_center() / (this.map_size / 2), 2),
                d: !this.env.in_bounds
            }
        return {
            o: null,
            r: 0,
            d: !this.env.in_bounds
        }
    }

    reset() {
        this.env = this.generate_env()
        return this.env;
    }
}

module.exports = {
    pilot: PilotMap
}