
var selected = document.querySelector(".time-periods #all");
selected.classList.add("selected");

for (const btn of document.querySelectorAll(".time-periods button")) {
    btn.onclick = () => {
        selected.classList.remove("selected");
        btn.classList.add("selected");
        selected = btn;
    }
}


let chart = document.querySelector('.chart canvas');

let data;
fetch("bengstock.pythonanywhere.com/get_data")
    .then(res => res.json())
    .then(d => data = d)

document.querySelector("#last-value").innerText = data.last;
document.querySelector("#daily-max").innerText = data.max;

//var gradientFill = chart.getContext("2d").createLinearGradient(0, 100, 0, 300);
//gradientFill.addColorStop(0, "#36dd87");
//gradientFill.addColorStop(1, "#3687dd00");



var lineChart = new Chart(chart, {
    type: "line",
    data: {
        labels: data.x,
        datasets: [{
            label: 'EuroStocks',
            data: data.y,
            fill: true,
            borderColor: '#36dd87',
            backgroundColor: "#36dd8780",
            tension: 0.1
        }]
        },
    options: {
        elements: {
            point: {
                radius: 0
            }
        },
        scales: {
            xAxes: [{
                gridLines: {
                    //show: false,
                    lineWidth: 5
                }
            }],
            yAxes: [{
                gridLines: {
                    //show: false,
                    lineWidth: 5
                }
            }]
        },
        maintainAspectRatio: false
    }
})

var width;
var height;

setInterval(() => {
    //console.log(width, window.innerWidth)
    if (width !== window.innerWidth || height !== window.innerHeight) {
        //console.log(chart.height, chart.parentNode.clientHeight);

        chart.width = chart.parentNode.clientWidth;
        chart.height = chart.parentNode.clientHeight;
        lineChart.resize();

        //console.log(chart.width, chart.height)

        width = window.innerWidth;
        height = window.innerHeight;
        lineChart.draw();
    }
}, 100);