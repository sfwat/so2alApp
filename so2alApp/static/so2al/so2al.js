document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#submitter').addEventListener('click', () => load_submit_form());
  document.querySelector("#submit-form").addEventListener('submit', submit_user);
  document.querySelector('#question').addEventListener('click', () => get_question());
  document.querySelector('#question-form').addEventListener('submit', submit_question)
  document.querySelector('#question-stats').addEventListener('click', () => get_question_stats());
  load_submit_form();
});


function load_submit_form() {
  // Show the submit view and hide other views
  document.querySelector('#submit-view').style.display = 'block';
  document.querySelector('#question-view').style.display = 'none';
  document.querySelector('#stats-view').style.display = 'none'
}

function get_question(sub_id=5) {
    let url = `/so2al/question?submitter_id=${sub_id}`
    fetch(url)
    .then(response => response.json())
     .then(question => {
            load_question(question)
    });
}


function load_question(question) {
    document.querySelector('#submit-view').style.display = 'none';
    document.querySelector('#question-view').style.display = 'block';
    document.querySelector('#stats-view').style.display = 'none'
    question_text = document.querySelector("#question-text")
    question_text.innerHTML = question.question
    question_text.value = question.id
    first_answer = document.querySelector("#first-answer")
    second_answer = document.querySelector("#second-answer")
    third_answer = document.querySelector("#third-answer")
    first_answer.value = question.choice[0].id
    second_answer.value = question.choice[1].id
    third_answer.value = question.choice[2].id
    first_answer_label = document.querySelector("#first-answer-label")
    second_answer_label = document.querySelector("#second-answer-label")
    third_answer_label = document.querySelector("#third-answer-label")
    first_answer_label.innerHTML = question.choice[0].choice_text
    second_answer_label.innerHTML = question.choice[1].choice_text
    third_answer_label.innerHTML = question.choice[2].choice_text

}

function get_question_stats(pk) {
    let url = `/so2al/question/${pk}`
    fetch(url)
    .then(response => response.json())
     .then(stats => {
            load_chart(stats.stats)
    });
}


function load_chart(stats) {
    document.querySelector('#submit-view').style.display = 'none';
    document.querySelector('#question-view').style.display = 'none';
    document.querySelector('#stats-view').style.display = 'block'
    const answers_count = [
          ['Choice', 'Count'],
        ]
     stats.forEach(function (item, index) {
                    answers_count.push([item.choice, item.count])
                });

    google.charts.load("current", {packages:["corechart"]});
    google.charts.setOnLoadCallback(drawChart);
      function drawChart() {
        var data = google.visualization.arrayToDataTable(answers_count);

        var options = {
          title: 'Answers stats',
          pieHole: 0.6,
          'width':750, 'height':500
        };

        var chart = new google.visualization.PieChart(document.getElementById('pie-chart'));
        chart.draw(data, options);
      }
}


function submit_user(e) {

    name = document.querySelector("#submit-name").value
    nationality = document.querySelector("#submit-nationality").value
    address = document.querySelector("#submit-address").value
    date_of_birth = document.querySelector("#submit-date").value
    gender = document.querySelector("#submit-gender").value

    fetch('/so2al/submitter/', {
    method: 'POST',
    body: JSON.stringify({
      name: name,
      nationality: nationality,
      address: address,
      date_of_birth: date_of_birth,
      gender: gender
        }),
    headers: new Headers({'content-type': 'application/json'})
    })
    .then(response => response.json())
    .then(result => {
        localStorage.setItem('userId', result.id);
        get_question(result.id);
});
      e.preventDefault();
}


function submit_question(e) {

        inputs = document.querySelectorAll('.form-check-input');
        for (var i = 0; i < inputs.length; i++) {
            if (inputs[i].checked === true) {
                add_answer(inputs[i].value)
                break
            }
        }
        e.preventDefault();

}


function add_answer(choice){
    question = document.querySelector("#question-text")
    question = question.value
    submitter = localStorage.getItem('userId')
    fetch('/so2al/answer/', {
    method: 'POST',
    body: JSON.stringify({
      question: question,
      submitter: submitter,
      choice: choice
        }),
    headers: new Headers({'content-type': 'application/json'})
    })
    .then(response => response.json())
    .then(result => {
        get_question_stats(question);
        });
}