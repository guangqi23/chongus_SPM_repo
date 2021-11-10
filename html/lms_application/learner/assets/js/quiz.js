//getting all required elements

const start_btn = document.querySelector(".start_btn button");
const info_box = document.querySelector(".info_box");
const exit_btn = info_box.querySelector(".buttons .quit");
const continue_btn = info_box.querySelector(".buttons .restart");
const quiz_box = document.querySelector(".quiz_box");
const option_list = document.querySelector(".option_list");
const timeCount = quiz_box.querySelector(".timer .timer_sec");
const timeLine = quiz_box.querySelector("header .time_line");
const quiz_title = document.getElementById('quiz_Title');

let timeValue;

timerURL = 'http://localhost:5000/get_Quiz_Timer?quiz_id=' + String(sessionStorage.getItem("quiz_id"));
axios.get(timerURL)
    .then(response => {
        console.log("Timer is:", response.data);
        timeValue = parseInt(response.data);
        //timeValue = 15; Use if want to test timeout function
    });

timerURL = 'http://localhost:5000/get_Section_Title?quiz_id=' + String(sessionStorage.getItem("quiz_id"));
axios.get(timerURL)
    .then(response => {
        console.log("Quiz title is: " , response.data);
        quiz_title.innerHTML = ("Section Quiz: " + String(response.data));
    });




//If Start Quiz Button is clicked
start_btn.onclick = ()=>{
    info_box.classList.add("activeInfo"); //Display info box
}

//If Exit button is clicked
exit_btn.onclick = ()=>{
    info_box.classList.remove("activeInfo"); //Hide info box
}

//If Continue Button is clicked
continue_btn.onclick = ()=>{
    info_box.classList.remove("activeInfo"); //Hide info box
    quiz_box.classList.add("activeQuiz"); //Show quiz box
    showQuestions(0);
    questionCounter(1);
    clearInterval(counter);
    startTimer(timeValue);
    //startTimerLine(counterLine); //Got bug
}

let question_count = 0;
let question_num = 1;
let counter;
let counterLine;

let widthValue = 0;
let userScore = 0;

const nxt_btn = quiz_box.querySelector('.nxt_btn');
const result_box = document.querySelector(".result_box");
const restart_quiz = result_box.querySelector(".buttons .restart");
const quit_quiz = result_box.querySelector(".buttons .quit");

restart_quiz.onclick = ()=>{
    // quiz_box.classList.add("activeQuiz");
    // result_box.classList.remove("activeResult");
    
    // let question_count = 0;
    // let question_num = 1;
    // let timeValue = 15;
    // let widthValue = 0;
    // let userScore = 0;
    // showQuestions(question_count);
    // questionCounter(question_num);
    // clearInterval(counter);
    // clearInterval(counterLine);
    // startTimer(timeValue);
    // startTimerLine(widthValue);
    // nxt_btn.style.display = "none";
    window.location.reload();
}

quit_quiz.onclick = ()=>{
    window.location.reload();
}

//If Next Button is clicked
nxt_btn.onclick = ()=>{

    if(question_count < questions.length - 1)
    {
        question_count++;
        question_num++;
        showQuestions(question_count);
        questionCounter(question_num);
        //startTimerLine(widthValue);
        nxt_btn.style.display = "none";
    }
    else
    {
        console.log("All questions completed!");
        showResultBox();
    }


}

//Get questions and options from array
function showQuestions(index){
    const question_text = document.querySelector(".question_text");
    
    // let question_tag = '<span>'+ questions[index].number + '. ' +questions[index].question + '</span>';
    let question_tag = '<span>'+ questions[index].question + '</span>';
    let option_tag
    if(String(questions[index].answer) == "true" || String(questions[index].answer) == "false")
    {
        option_tag = '<div class="option">'+questions[index].options[0]+'<span></span></div>'
                       + '<div class="option">'+questions[index].options[1]+'<span></span></div>';
    }
    else
    {
        option_tag = '<div class="option">'+questions[index].options[0]+'<span></span></div>'
                    + '<div class="option">'+questions[index].options[1]+'<span></span></div>'
                    + '<div class="option">'+questions[index].options[2]+'<span></span></div>'
                    + '<div class="option">'+questions[index].options[3]+'<span></span></div>';
    }
    
    question_text.innerHTML = question_tag;
    option_list.innerHTML = option_tag;
    const option = option_list.querySelectorAll(".option");
    for(let i = 0; i < option.length; i++)
    {
        option[i].setAttribute("onclick","optionSelected(this)");
    }
}

let tickIcon = '<div class="icon tick"><i class="fas fa-check"></i></div>';
let crossIcon = '<div class="icon cross"><i class="fas fa-times"></i></div>';

function optionSelected(answer)
{
    let userAns = String(answer.textContent);
    console.log("Selected option:" , userAns);
    let correctAns = String(questions[question_count].answer);
    let allOptions = option_list.children.length; //Can reuse 
    console.log("Comparing: " , userAns, " vs " , correctAns);
    if(userAns == correctAns)
    {
        userScore += 1;
        console.log(userScore);
        answer.classList.add("correct");
        console.log("Correct!");
        answer.insertAdjacentHTML("beforeend", tickIcon);
    }
    else
    {
        answer.classList.add("wrong");
        console.log("Wrong!");

        //If answers is incorrect then automatically show the correct answer
        for (let i = 0; i < allOptions; i++)
        {
            if(option_list.children[i].textContent == correctAns)
            {
                option_list.children[i].setAttribute("class","option correct");
            }
        }
    }
    
    //Disable all other options once user select one
    for (let i = 0; i < allOptions; i++)
    {
        option_list.children[i].classList.add("disabled");
    }

    nxt_btn.style.display = "block";

}

function showResultBox()
{
    info_box.classList.remove("activeInfo"); //Hide info
    quiz_box.classList.remove("activeQuiz"); //Hide quiz
    result_box.classList.add("activeResult"); //Show result
    const scoreText = result_box.querySelector(".score_text");
    let percentage = (userScore / questions.length) * 100;

    //scoreObj = [sessionStorage["quiz_id"], sessionStorage["learner_id"] , percentage];
    if(userScore == questions.length)
    {
        let scoreTag = '<span>Congratulations, you got <p>'+ userScore +'</p> out of <p>' +questions.length+ '</p></span>'
        scoreText.innerHTML = scoreTag;
    }
    else if(userScore >= (questions.length / 2))
    {
        let scoreTag = '<span>Nice, you got only <p>'+ userScore +'</p> out of <p>' +questions.length+ '</p></span>'
        scoreText.innerHTML = scoreTag;
    }
    else
    {
        let scoreTag = '<span>Sorry, you got only <p>'+ userScore +'</p> out of <p>' +questions.length+ '</p></span>'
        scoreText.innerHTML = scoreTag;
    }
    var ungradSubmitUrl = new URL('http://localhost:5000/submitScore');
    ungradSubmitUrl.search = new URLSearchParams({quiz_id: sessionStorage["quiz_id"] , user_id : sessionStorage["learner_id"], score: percentage})
    
    axios.post(ungradSubmitUrl)
                .then(response => {
                    console.log()
                });

    
}



function startTimer(time)
{
    counter = setInterval(timer, 1000);
    console.log(counter);
    function timer(){
        timeCount.textContent = time;
        time--;
        if(time < 9)
        {
            let addZero = timeCount.textContent;
            timeCount.textContent = "0" + addZero;
        }

        if(time < 0)
        {
            clearInterval(counter);
            showResultBox();
        }
    }
}

function startTimerLine(time)
{
    counterLine = setInterval(timer, 50);
    console.log(counter);
    function timer(){
        time += 1;
        timeLine.style.width = time + "px";
        if(time > 600)
        {
            clearInterval(counterLine)
        }

        
    }
}




function questionCounter(index)
{
    const bottom_question_counter = quiz_box.querySelector(".total_que");
    let totalQuestionCount = '<span><p>'+ question_num +'</p>of<p>' + questions.length + '</p>Questions</span>';
    bottom_question_counter.innerHTML = totalQuestionCount;
}