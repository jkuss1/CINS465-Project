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
		
		if (element.offsetLeft - x < 0)
			element.style.left = "0px";
		else if(element.offsetLeft + element.offsetWidth > window.innerWidth)
			element.style.left = (window.innerWidth - element.offsetWidth) + "px";
		
		if (element.offsetTop - y < 0)
			element.style.top = "0px";
		else if(element.offsetTop + element.offsetHeight > window.innerHeight)
			element.style.top = (window.innerHeight - element.offsetHeight) + "px";
	}

	function stopDrag()
	{
		element.x = element.offsetLeft;
		element.y = element.offsetTop;
		document.onmousemove = null;
		document.onmouseup = null;
	}
}
/* [END] Draggable Element */


var calcShown = false;
function toggleCalculator()
{
	var calc = document.getElementById("calc");

	if (calcShown)
	{
		calc.style = "display: none";
		calcShown = false;
	}
	else
	{
		calc.style = "display: inline";
		calc.style.left = calc.x + "px";
		calc.style.top = calc.y + "px";
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

$("#calc-close").click(function() {
	toggleCalculator();
});

dragElement(document.getElementById("calc"));


function dateChange(self)
{
	if (self.value.match("/")) {
		date = self.value.split("/");
		self.value = date[2] + "-" + date[0] + "-" + date[1] + " 0:00";
	}
}


$("#del-item-form").on("submit", function(e) {
	e.preventDefault();

	var name = $("#del-item-form-name").val();
	
	if (confirm("Delete \"" + name + "\"")) {
		$.ajax({
			'type': "POST",
			'url': "http://" + window.location.host + "/account/delete_item/" + $("#del-item-form-id").val() + "/",
			'data': $("#del-item-form").serialize(),
			'success': function() {
				$("#del-item-form").parent().remove();
			},
			'error': function() {
				alert("Unable to delete \"" + name + "\".\nPlease try again.");
			}
		})
	}
});

var timeout;
function searchItems(keyword)
{
	clearTimeout(timeout);
	
	timeout = setTimeout(function() {
		var url;

		if (keyword) {
			url = "http://" + window.location.host + "/search_items/" + keyword + "/";
		}
		else {
			url = "http://" + window.location.host + "/get_popular_items/";
		}
		
		$.ajax({
			'url': url,
			'success': function(data) {
				var json = JSON.parse(data);

				var allItemsCont = document.getElementById("all-items-cont");
				allItemsCont.innerHTML = "";

				for (var i = 0; i < json.length; i++) {
					var item = json[i];

					var cont = document.createElement("div");
					allItemsCont.appendChild(cont);
					
					var itemCont = document.createElement("div");
					itemCont.classList.add("item-cont");
					cont.appendChild(itemCont);

					var name = document.createElement("h3");
					name.innerHTML = item.name;
					itemCont.appendChild(name);
					
					for (var j = 0; j < item.images.length; j++) {
						var image = item.images[j];
						
						var img = document.createElement("img");
						img.classList.add("img-cont");
						img.src = image.url;
						img.alt = image.alt;
						itemCont.appendChild(img);
					}

					var p = document.createElement("p");
					itemCont.appendChild(p);

					var strong = document.createElement("strong");
					strong.innerHTML = "Item Details: "
					p.appendChild(strong);
					
					p.innerHTML += item.details + "&emsp;&emsp;&emsp;";

					strong = document.createElement("strong");
					strong.innerHTML = "Cost Per Item: "
					p.appendChild(strong);

					p.innerHTML += item.cost + "&emsp;&emsp;&emsp;";
					
					strong = document.createElement("strong");
					strong.innerHTML = "Total Available: "
					p.appendChild(strong);
					
					p.innerHTML += item.units_available;

					if (item.sale_start && item.sale_end) {
						p = document.createElement("p");
						itemCont.appendChild(p);

						strong = document.createElement("strong");
						strong.innerHTML = "Sale Start: "
						p.appendChild(strong);
						
						p.innerHTML += item.sale_start + "&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;";

						strong = document.createElement("strong");
						strong.innerHTML = "Sale End: "
						p.appendChild(strong);
						
						p.innerHTML += item.sale_end;
					}

					if (item.discount_start && item.discount_end) {
						p = document.createElement("p");
						itemCont.appendChild(p);

						strong = document.createElement("strong");
						strong.innerHTML = "Discount Start: "
						p.appendChild(strong);
						
						p.innerHTML += item.discount_start + "&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;";

						strong = document.createElement("strong");
						strong.innerHTML = "Discount End: "
						p.appendChild(strong);
						
						p.innerHTML += item.discount_end;
					}

					var hr = document.createElement("hr");
					itemCont.appendChild(hr);
				}
			}
		})
	}, 500);
}