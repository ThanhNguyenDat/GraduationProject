window.addEventListener("DOMContentLoaded",function(){
	var canvas=document.getElementById("canvas"),
		video=document.getElementById("video"),
		context=canvas.getContext("2d"),
		videoObj={"video":true},
		errorfn=function(){
		console.log('str wrong');
	}
	var play=function(){
		if(navigator.getUserMedia) { // Standard
			navigator.getUserMedia(videoObj, function(stream) {
				video.src = stream;
				video.play();
			}, errorfn);
		} else if(navigator.webkitGetUserMedia) { // WebKit-prefixed
			navigator.webkitGetUserMedia(videoObj, function(stream){
				video.src = window.webkitURL.createObjectURL(stream);
				video.play();
			}, errorfn);
		} else if(navigator.mozGetUserMedia) { // WebKit-prefixed
			navigator.mozGetUserMedia(videoObj, function(stream){
				video.src = window.URL.createObjectURL(stream);
				video.play();
			}, errorfn);
		}
		else if(navigator.msGetUserMedia) { // WebKit-prefixed
			navigator.mozGetUserMedia(videoObj, function(stream){
				video.src = window.URL.createObjectURL(stream);
				video.play();
			}, errorfn);
		}
	}
	play();
	document.getElementById("picture").addEventListener("click",function(){
		context.drawImage(video,0,0,640,480);
	})
},false)