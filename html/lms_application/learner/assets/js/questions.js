//Create an array and passing the number, questions, options and answers
//Retrieve info from db

microServiceURL = "http://localhost:5000/get_Quiz_Questions_Options?quiz_id=" + String(sessionStorage.getItem("quiz_id"));
let request = new XMLHttpRequest();
request.open('GET',microServiceURL);
request.responseText = 'text';
let allQuestions;


let questions
request.onload = function() 
{
    allQuestions = JSON.parse(request.responseText);
    console.log(allQuestions);
    //console.log(allQuestions["data"][0]["qorder"]) //Access method

    for( let a = 0; a < allQuestions["data"].length; a++)
    {
        console.log("Loop num: " , a);
        console.log(allQuestions["data"][a]["qorder"]);
        console.log(allQuestions["data"][a]["question"]);
        console.log(allQuestions["data"][a]["question_type"]);
        console.log(allQuestions["data"][a]["question_id"]);
        let questionType = allQuestions["data"][a]["question_type"]
        let questionId = allQuestions["data"][a]["question_id"];

        //Empty dicObj
        //let questionObj = [{number: allQuestions["data"][a]["qorder"], question: allQuestions["data"][a]["question"]}]
        let questionObj = {}
        if(questionType == "MCQ")
        {
            console.log("MCQ found!");
            mcqURL = "http://localhost:5000/get_MCQ?question_id=" + questionId;



            //Current issue: order of questions are not consistent in displaying on quiz page

            let mcqRequest = new XMLHttpRequest();
            mcqRequest.open("GET", mcqURL);
            mcqRequest.send();

            mcqRequest.onreadystatechange = function() {
                if(this.readyState == 4 && this.status == 200)
                {
                    allOptions = JSON.parse(mcqRequest.responseText);
                    if(allOptions["data"] != null)
                    {
                        console.log(allOptions["data"]);
                        record = allOptions["data"];

                        //Must always have 4 options
                        qOptions = [record[0]["option_content"], record[1]["option_content"], record[2]["option_content"], record[3]["option_content"]];
                        console.log("All options: " , qOptions);
                        for(let b = 0; b < record.length; b++)
                        {
                            if(record[b]["correct_option"] === true)
                            {
                                console.log(record[b]["correct_option"]);
                                questionObj["answer"] = record[b]["option_content"];
                                console.log(questionObj["answer"]);
                            }
                        }

                        questionObj["options"] = qOptions;


                        questionObj["number"] = allQuestions["data"][a]["qorder"];
                        questionObj["question"] = allQuestions["data"][a]["question"];
                        console.log(questionObj);
                        questions.push(questionObj);
                    }
                    
                }
                
            
            }



            
        }
        else if (questionType == "TF")
        {
            tfURL = 'http://localhost:5000/get_TrueFalse?question_id=' + questionId;
            axios.get(tfURL)
                .then(response => {
                    dataArr = response.data["data"][0];
                    console.log("LMAO", dataArr);
                    console.log("LMAO", dataArr["answer"]);
                    questionObj["answer"] = dataArr["answer"]
                    questionObj["options"] =  ["true", "false"];
                    questionObj["number"] = dataArr["qorder"];
                    questionObj["question"] = dataArr["question"];
                    console.log(questionObj);
                    questions.push(questionObj);
                });
        }
        
    }//end of for loop


    questions=[
    ];

}; //End of request
request.send();





