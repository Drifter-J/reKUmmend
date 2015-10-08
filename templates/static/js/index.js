var userInfoArray = {}; // user 정보를 담고있는 객체 
var isInitializeFinished = false;

/**
 * 최초 진입 부분 
 */
var init = function(){    
	$("#loginBox").fadeIn(1500); // login box fade in
	
	initLoginFunctions();	
};

/**
 * Login 동작에 필요한 함수들 초기화 
 */
var initLoginFunctions = function(){
	
	/**
	 * enter 입력 시 login 처리 
	 */
	$("#loginBoxPW").keypress(function(e) {
		if(e.keyCode == 13 || e.which == 13){

			doLoginProcess();
		}
	});
	
	/**
	 * login 버튼 click 이벤트 
	 */
	$("#loginBoxEnter").click(function(){
		doLoginProcess();
	});
	
	/**
	 * 서버와 login 통신 처리 
	 */
	var doLoginProcess = function(){
		
		var data = {
				"userId": $("#userId").val(),
				"userPw": $("#userPw").val()
		};

		$("#mainPageTransparentLayer").show();
		$("#headerSignUp").hide();
		$("#headerLogOut").show();
		$("#backgroundBlur").fadeOut(700, function() {});
		$("#loginBox").fadeOut(600, function() {  // login box fade out
						
			currentTabPage = "mainPageContentsMyLibrary";
            $("#mainPageHeaderMyLibrary").css({"font-weight": "bold", "color": "#045FB4"});
            $("#mainPageHeaderStore").css({"font-weight": "normal", "color": "#FFF"});
            $("#mainPageHeaderHWPurchase").css({"font-weight": "normal", "color": "#FFF"});
						
			$("#mainPageSearchContainer").show();
						
			$("#mainPageContentsMyLibrary").show();
			$("#mainPageContentsStore").hide();
			$("#mainPageContentsHWPurchase").hide();
						
			$("#paymentBoxArea").hide();
			$("#descriptionBox").hide();
			$("#validPwBox").hide();
						
			$("#mainPageArea").fadeIn(300, function() {
				$("#mainPageTransparentLayer").hide();
			});

		}).queue(function(){

			$("#loadingBox").show();
			$("#loadingGif").fadeIn(800);
		});
		
		

		
			
		
		
	};
};
