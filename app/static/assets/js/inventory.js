// Add push (to store answers)
var score=0;
var q = 0,
	 textLongEnough = false,
	 flagMulti = false,
	 paramHTML = "";
	
$(function() {
	$("#wrap").fadeIn(500);
	welcomeScreen();
	navButtons();
	
	$("#qBox").on("click", ".begin", function () {
		reset();
	});
	
	$("#aBox").on("click", ".single", function(event) {
		if ($("#wrap").hasClass("paused") === false) {
			// Handles trigger questions
			if ($(this).hasClass("helpWithWebsite")) {
				 qa[1].cssQ = "text";
			} else {
                console.log(event.target.id);
                score+=parseInt(event.target.id);
				singleClicked();
			}
		}
	});
	
	// Handles typing in textarea
	$("#aBox").on("keyup", ".textArea", function(e) {
		var numChars = $(".textArea").val().length;
		var minChars = 10;
		var submitMarkup = "<div class='inputNext'>Submit</div>";
		var submitClass = ".inputNext";
		
		$(".textCounter").html(numChars + " chars");
		
		if ($("#wrap").hasClass("paused")) {
			e.preventDefault();
		} else {
			checkLength(numChars, minChars, submitMarkup, submitClass);
		}
	});
	
	// Submit textarea
	$("#submitBox").on("click", ".inputNext", function() {
		if ($("#wrap").hasClass("paused") === false) {
			inputClicked();
		}
	});
		
	// Handles typing in text input
	$("#aBox").on("keyup", "input", function(e) {
		var numChars = $("input").val().length;
		var minChars = 4;
		var submitMarkup = "<div class='textNext'>Submit</div>";
		var submitClass = ".textNext";
		
		checkLength(numChars, minChars, submitMarkup, submitClass);
	});
	
	// Submit text input
	$("#submitBox").on("click", ".textNext", function() {
		if ($("#wrap").hasClass("paused") === false) {
			if ($("input").hasClass("url")) {
				var inputValue = $(".url").val();
				var inputPre = inputValue.slice(0, 4);

				if (inputPre === "http") {
					var inputSplit = inputValue.split("://");
					inputPre = inputSplit[1].slice(0, 4);
					inputValue = inputSplit[1];
				}								
				if (inputPre != "www.") {
					inputValue = "www." + inputValue;
				}

				var firstDotPos = inputValue.indexOf(".");
				var lastDotPos = inputValue.lastIndexOf(".");
				var textLength = inputValue.length;

				if ((firstDotPos === lastDotPos) || (lastDotPos === - 1) || ((lastDotPos + 2) >= textLength)) {
					$("#error").html("That isn't a valid URL.<br>Please enter the address of the website.");
				} else {
					$("#error").html("");
					textLongEnough = false;
					reset();
				}	
			} else {
				reset();
			}
		}
	});
		
	// Handles multiple choice selection
	$("#aBox").on("click", ".multiple", function() {
		if ($("#wrap").hasClass("paused") === false) {
			if ($(this).hasClass("selected")) {
				$(this).removeClass("selected");
				$(this).css("background-color", "#fefefe");
				$(this).css("color", "#403e30");
				$(this).find("i").removeClass("fa-check-square-o");
				$(this).find("i").addClass("fa-square-o");
			} else {
				$(this).addClass("selected");
				$(this).css("background-color", "#00a1e4");	
				$(this).css("color", "#eee");
				$(this).find("i").removeClass("fa-square-o");
				$(this).find("i").addClass("fa-check-square-o");
			}

			if ($(".answers").hasClass("selected")) {
				if (flagMulti === false) {
					$("<div class='multipleDone'>Submit</div>").hide().appendTo("#submitBox").fadeIn(500);
					$("#error").html("");
					flagMulti = true;
				}
			} else {
				$(".multipleDone").remove();
				$("#error").html("Please select at least one answer");
				flagMulti = false;
			}
		}
	});
					  
	// Submit multiple choice
	$("#submitBox").on("click", ".multipleDone", function() {
		if ($("#wrap").hasClass("paused") === false) {
			multiClicked();
		}
	});
	
	// Back button
	$("#backIcon").on("click", function() {
		if ($("#wrap").hasClass("paused") === false) {
			back();
		}
	});
	
	// Fwd button
	$("#fwdIcon").on("click", function() {
		if ($("#wrap").hasClass("paused") === false) {
			fwd();
		}
	});

	// Exit button
	$("#exit").on("click", function() {
		if ($("#wrap").hasClass("paused") === false) {
			quit();
		}
	});
	
	// Reopen questionnaire
	$("#qOpen").on("click", function() {
	//$("#qOpen").click(function() {
		reOpen();
	});
	
	// Erase Answers and Start Over
	$("#startOver").on("click", function () {
		verifyStartOver();
	});
	
	// Start Over = Cancel
	$("#startOverNo").on("click", function() {
		$("#verifyBox").animate({opacity: "0"}, 150);
		$("#wrap").removeClass("blurred");
		$("#wrap").removeClass("paused");
		$('.text').prop('readonly', false);
	});
	
	// Star Over = Yes
	$("#startOverYes").on("click", function() {
		startOver();
	});
}); // end DOM ready function


/***** 
Functions 
******/

function welcomeScreen() {
	$("#backIcon").hide();
	
	$("<div id='welcome'><h1>Depression Detection Inventory</h1>The following assessment will take between 10-15 minutes of your time. It will help me determine your depression level.</div><div class='begin'>Begin</div>").hide().appendTo("#qBox").fadeIn(500);
}

function nextQuestion() {
    if(q==20){
        q+=1;
        var payload = {
            'score':score,
            'email':1
        }; 
        $.post("/inventory/",payload);

        // location.href = "/dashboard/";
        $("<div class='question'></div>").hide().appendTo("#qBox").fadeIn(500);
	    $(".question").html("<img src='../static/assets/img/loading.gif' %}' style='width:50%;'><p>Calculating Results<p>");
        setTimeout(function () {
            var str=""
            if(score==0){
                str="<p>Unable to evaluate. Try Again.</p>";
            }
            else if(score>0 && score<11){
                str="<p>Aggregate Score: " + String(score) + "</p><h3>These ups and downs are considered normal.</h3>";
            }
            else if(score>10 && score<17){
                str="<p>Aggregate Score: " + String(score) + "</p><h3>Mild Mood Disturbance</h3>";
            }
            else if(score>16 && score<21){
                str="<p>Aggregate Score: " + String(score) + "</p><h3>Borderline Clinical Depression</h3>";
            }
            else if(score>20 && score<31){
                str="<p>Aggregate Score: " + String(score) + "</p><h3>Moderate Depression</h1>";
            }
            else if(score>30 && score<41){
                str="<p>Aggregate Score: " + String(score) + "</p><h3>Severe Depression</h3>";
            }
            else{
                str="<p>Aggregate Score: " + String(score) + "</p><h3>Extreme Depression</h3>";
            }
            str += "<a class='abegin' style='font-size:0.8em; text-decoration:none;' href='/dashboard/';>Go Back</a>";
            $(".question").html(str);
        }, 5000);
    }
    else{
        var qClass = qa[q].cssQ;
        $("<div class='question'></div>").hide().appendTo("#qBox").fadeIn(500);
        $(".question").html(qa[q].question);
        $(".question").addClass(qClass);
        
        for(i = 0; i < qa[q].answers.length; i++) {
            var aClass = qa[q].cssA[i];
            var answer = qa[q].answers[i];
            
            $("<div id=" + aClass + " class='answers " + qClass + " " + aClass + "'>" + answer + "</div>").hide().appendTo("#aBox").fadeIn(900);
            };
            if (qClass === "multiple") {
                $("<i class='fa fa-square-o'></i> ").hide().prependTo(".answers").fadeIn(900);
            } else if (qClass === "input") {
                $("<div class='textCounter'></div>").appendTo(".answers");
            }
        q += 1;
        navButtons();
    }
}

function singleClicked() {
	// store answer
	reset();
}

function inputClicked() {
	// store answer
	textLongEnough = false;
	reset();
}

function multiClicked() {
	// store answer
	flagMulti = false;
	reset();
}

// Check textarea and text input
function checkLength(numChars, minChars, submitMarkup, submitClass) {
	$(".textCounter").addClass("red");
	if (numChars < minChars) {
		if (textLongEnough === true) {
			$(submitClass).remove();
			$("#error").html("Your answer is too short");
			textLongEnough = false;
		} 
	} else if ((numChars = minChars) || (numChars > minChars)) {
		$(".textCounter").removeClass("red");
		if (textLongEnough === false) {
			$("#error").html("");
			$(submitMarkup).hide().appendTo("#submitBox").fadeIn(500);
			textLongEnough = true;
		}
	}
}

function reset() {
	$("#welcome").remove();
	$(".begin").remove();
	$(".question").remove();
	$(".answers").remove(); 
	$(".inputNext").remove();
	$(".textURLNext").remove();
	$(".textNext").remove();
	$(".multipleDone").remove();
	$("#error").html("");
	nextQuestion();
}
	
function quit() {
	$("#wrap").hide();
	$("#qOpen").animate({bottom:"0px"}, 200);
}

function reOpen() {
	$("#wrap").fadeIn();
	$("#qOpen").animate({bottom:"-50px"}, 200);
}

function back() {
	q = q - 2;
	navButtons();
	reset();
}

function fwd() {
	navButtons();
	reset();
}

function navButtons() {
	if (q > 0) {
		$("#backIcon").fadeIn(400);
	} else if (q === qa.length) {
		$("#fwdIcon").hide();
	} else if (q < 0) {
		// fix this
		$("#fwdIcon").fadeIn(400);			  
	} else {
		$("#backIcon").hide();
	}
}

function verifyStartOver() {
	window.scrollTo(0, 0);
	$("#wrap").addClass("blurred");
	$("#wrap").addClass("paused");
	$('.text').prop('readonly', true);
	$("#verifyBox").animate({opacity: "1"}, 150);
}
	
function startOver() {
	var q = 0;
	textLongEnough = false;
	flagMultiple = false;
	paramHTML = "";
	$("#verifyBox").animate({opacity: "0"}, 150);
	$("#wrap").removeClass("blurred");
	$("#wrap").removeClass("paused");
	reset();
}
	
//var storeAnswers = new Array();
		

/***** 
Questions 
******/
				
var qa = [
	{cssQ: "single", question: "Select one of the below options.", answers: ["I do not feel sad.", "I feel sad.", "I am sad all the time and I can't snap out of it.", "I am so sad and unhappy that I can't stand it."], cssA: ["0", "1", "2", "3"]},
    {cssQ: "single", question: "Select one of the below options.", answers: ["I am not particularly discouraged about the future.", "I feel discouraged about the future.", "I feel I have nothing to look forward to.", "I feel the future is hopeless and that things cannot improve."], cssA: ["0", "1", "2", "3"]},
    {cssQ: "single", question: "Select one of the below options.", answers: ["I do not feel like a failure.", "I feel I have failed more than the average person.", "As I look back on my life, all I can see is a lot of failures.", "I feel I am a complete failure as a person."], cssA: ["0", "1", "2", "3"]},
    {cssQ: "single", question: "Select one of the below options.", answers: ["I get as much satisfaction out of things as I used to.", "I don't enjoy things the way I used to.", "I don't get real satisfaction out of anything anymore.", "I am dissatisfied or bored with everything."], cssA: ["0", "1", "2", "3"]},
    {cssQ: "single", question: "Select one of the below options.", answers: ["I don't feel particularly guilty.", "I feel guilty a good part of the time.", "I feel quite guilty most of the time.", "I feel guilty all of the time."], cssA: ["0", "1", "2", "3"]},
    {cssQ: "single", question: "Select one of the below options.", answers: ["I don't feel I am being punished.", "I feel I may be punished.", "I expect to be punished.", "I feel I am being punished."], cssA: ["0", "1", "2", "3"]},
    {cssQ: "single", question: "Select one of the below options.", answers: ["I don't feel disappointed in myself.", "I am disappointed in myself.", "I am disgusted with myself.", "I hate myself."], cssA: ["0", "1", "2", "3"]},
    {cssQ: "single", question: "Select one of the below options.", answers: ["I don't feel I am any worse than anybody else.", "I am critical of myself for my weaknesses or mistakes.", "I blame myself all the time for my faults.", "I blame myself for everything bad that happens."], cssA: ["0", "1", "2", "3"]},
    {cssQ: "single", question: "Select one of the below options.", answers: ["I don't have any thoughts of killing myself.", "I have thoughts of killing myself, but I would not carry them out.", "I would like to kill myself.", "I would kill myself if I had the chance."], cssA: ["0", "1", "2", "3"]},
    {cssQ: "single", question: "Select one of the below options.", answers: ["I don't cry any more than usual.", "I cry more now than I used to.", "I cry all the time now.", "I used to be able to cry, but now I can't cry even though I want to."], cssA: ["0", "1", "2", "3"]},
    {cssQ: "single", question: "Select one of the below options.", answers: ["I am no more irritated by things than I ever was.", "I am slightly more irritated now than usual.", "I am quite annoyed or irritated a good deal of the time.", "I feel irritated all the time."], cssA: ["0", "1", "2", "3"]},
    {cssQ: "single", question: "Select one of the below options.", answers: ["I have not lost interest in other people.", "I am less interested in other people than I used to be.", "I have lost most of my interest in other people.", "I have lost all of my interest in other people."], cssA: ["0", "1", "2", "3"]},
    {cssQ: "single", question: "Select one of the below options.", answers: ["I make decisions about as well as I ever could.", "I put off making decisions more than I used to.", "I have greater difficulty in making decisions more than I used to.", "I can't make decisions at all anymore."], cssA: ["0", "1", "2", "3"]},
    {cssQ: "single", question: "Select one of the below options.", answers: ["I don't feel that I look any worse than I used to.", "I am worried that I am looking old or unattractive.", "I feel there are permanent changes in my appearance that make me look unattractive.", "I believe that I look ugly."], cssA: ["0", "1", "2", "3"]},
    {cssQ: "single", question: "Select one of the below options.", answers: ["I can work about as well as before.", "It takes an extra effort to get started at doing something.", "I have to push myself very hard to do anything.", "I can't do any work at all."], cssA: ["0", "1", "2", "3"]},
    {cssQ: "single", question: "Select one of the below options.", answers: ["I can sleep as well as usual.", "I don't sleep as well as I used to.", "I wake up 1-2 hours earlier than usual and find it hard to get back to sleep.", "I wake up several hours earlier than I used to and cannot get back to sleep."], cssA: ["0", "1", "2", "3"]},
    {cssQ: "single", question: "Select one of the below options.", answers: ["I don't get more tired than usual.", "I get tired more easily than I used to.", "I get tired from doing almost anything.", "I am too tired to do anything."], cssA: ["0", "1", "2", "3"]},
    {cssQ: "single", question: "Select one of the below options.", answers: ["My appetite is no worse than usual.", "My appetite is not as good as it used to be.", "My appetite is much worse now.", "I have no appetite at all anymore."], cssA: ["0", "1", "2", "3"]},
    {cssQ: "single", question: "Select one of the below options.", answers: ["I haven't lost much weight, if any, lately.", "I have lost more than five pounds.", "I have lost more than ten pounds.", "I have lost more than fifteen pounds."], cssA: ["0", "1", "2", "3"]},
    {cssQ: "single", question: "Select one of the below options.", answers: ["I am no more worried about my health than usual.", "I am worried about physical problems like aches, pains, upset stomach, or constipation.", "I am very worried about physical problems and it's hard to think of much else.", "I am so worried about my physical problems that I cannot think of anything else."], cssA: ["0", "1", "2", "3"]},
];
