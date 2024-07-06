$(document).ready(function () {
    var predictionText = "{{ prediction_text }}";
    var isEligible = predictionText.includes("Congratulations!");

    if (isEligible) {

        for (var i = 0; i < 50; i++) {
            var paper = document.createElement('div');
            paper.classList.add('paper');
            paper.style.left = Math.random() * window.innerWidth + 'px';
            document.body.appendChild(paper);
        }
    }
});
