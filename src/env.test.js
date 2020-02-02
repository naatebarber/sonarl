var assert = require("assert");
var env = require("./env");
var SonarEnv = new env.SonarEnv();

describe("env.SonarEnv", () => {
    it("starts with random motor input when none given", () => {
        assert.equal(Array.isArray(SonarEnv.motor_input_values), true)
        assert.equal(typeof (SonarEnv.motor_input_values.reduce((a, b) => a+b)), "number")
    })
    it("generates random actions", () => {
        var action = SonarEnv.sample_random_action();
        assert.equal(Array.isArray(action), true)
        assert.equal(typeof (action.reduce((a, b) => a+b)), "number")
    });
    it("returns ORDI on reset", () => {
        var ordi = SonarEnv.reset();
        assert.equal(typeof (ordi[0].reduce((a, b) => a + b)), "number")
        assert.equal(typeof ordi[1], "number")
        assert.equal(typeof ordi[2], "boolean")
    })
    it("returns ORDI when prompted", () => {
        var ordi = SonarEnv.get_observation();
        assert.equal(typeof (ordi[0].reduce((a, b) => a + b)), "number")
        assert.equal(typeof ordi[1], "number")
        assert.equal(typeof ordi[2], "boolean")
    })
    it("returns updated ORDI with step", () => {
        var ordi = SonarEnv.step(SonarEnv.sample_random_action());
        assert.equal(Array.isArray(ordi), true)
        assert.equal(typeof (ordi[0].reduce((a, b) => a + b)), "number")
        assert.equal(typeof ordi[1], "number")
        assert.equal(typeof ordi[2], "boolean")
        assert.equal(isNaN(ordi[0].reduce((a, b) => a + b)), false)
    })
});