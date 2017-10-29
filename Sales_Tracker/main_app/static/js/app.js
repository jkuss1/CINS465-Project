$(document).foundation()

/* Draggable Element */
function dragElement(element)
{
	var x = 0, y = 0, cX = 0, cY = 0;
	
	if (document.getElementById(element.id + "-header"))
		document.getElementById(element.id + "-header").onmousedown = dragMouseDown;
	else
		element.onmousedown = dragMouseDown;
	
	function dragMouseDown(e)
	{
		e = e || window.event;
		
		cX = e.clientX;
		cY = e.clientY;
		
		document.onmousemove = startDrag;
		document.onmouseup = stopDrag;
	}

	function startDrag(e)
	{
		e = e || window.event;
		
		x = cX - e.clientX;
		y = cY - e.clientY;
		cX = e.clientX;
		cY = e.clientY;

		element.style.left = (element.offsetLeft - x) + "px";
		element.style.top = (element.offsetTop - y) + "px";
	}

	function stopDrag()
	{
		document.onmousemove = null;
		document.onmouseup = null;
	}
}
/* [END] Draggable Element */


var calcShown = false;
function toggleCalculator()
{
	var calc = document.getElementById("calc");

	if (calcShown) {
		calc.style = "display: none";
		calcShown = false;
	}
	else {
		calc.style = "display: inline";
		calcShown = true;
	}
}

$(".calc-btn").click(function() {
	var calcInput = document.getElementById("calc-input");

	if ($(this).html() == "=")
		calcInput.value = eval(calcInput.value);
	else if ($(this).html() == "C")
		calcInput.value = "";
	else
		calcInput.value += $(this).html();
});

dragElement(document.getElementById("calc"));