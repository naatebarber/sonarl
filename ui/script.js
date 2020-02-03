$(document).ready(() => {
    $(".run-agent span").on("click", () => {
        $.post("/run-agent", data => {
            $(".run-agent-log").css("display", "block").html(data)
            $(".run-agent").remove()
        }); 
    })
});