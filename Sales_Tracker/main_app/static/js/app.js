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
		calc.style.display = "none";
		calcShown = false;
	}
	else
	{
		calc.style.display = "inline";
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

function deleteItem(form)
{
	var formID = form.id.split("-");
	var id = formID[3];
	var name = formID[4];
	
	if (confirm("Delete \"" + name + "\"")) {
		$.ajax({
			'type': "POST",
			'url': "http://" + window.location.host + "/account/delete_item/" + id + "/",
			'data': $("#" + form.id).serialize(),
			'success': function() {
				$("#" + form.id).parent().remove();
			},
			'error': function() {
				alert("Unable to delete \"" + name + "\".\nPlease try again.");
			}
		})
	}
	
	return false;
}

function addToCart(form)
{
	var btn = document.getElementById(form.id + "-btn");

	if (btn.value != "Added to Cart") {
		var id = form.id.split("-")[4];
		
		$.ajax({
			type: "POST",
			url: "http://" + window.location.host + "/account/add_to_cart/" + id + "/",
			data: $("#" + form.id).serialize(),
			success: function() {
				btn.style.backgroundColor = "darkgreen";
				btn.value = "Added to Cart";
			},
			error: function() {
				btnText = btn.value;
				btnColor = btn.style.backgroundColor;
				btn.style.backgroundColor = "darkred";
				btn.value = "Unable to Add to Cart";

				setTimeout(function() {
					btn.style.backgroundColor = btnColor;
					btn.value = btnText;
				}, 2000);
			}
		});
	}
	
	return false;
}

function delFromCart(form)
{
	var id = form.id.split("-")[4];
	
	$.ajax({
		type: "POST",
		url: "http://" + window.location.host + "/account/delete_from_cart/" + id + "/",
		data: $("#" + form.id).serialize(),
		success: function() {
			$("#" + form.id).parent().remove();
			
			var cartNumItems = document.getElementById("cart-num-items");
			cartNumItems.innerHTML = cartNumItems.innerHTML - 1;
		},
		error: function() {
			alert("Unable to remove from cart.\nPlease try again.")
		}
	});
	
	return false;
}

function checkout(form)
{
	if (document.getElementById("cart-num-items").innerHTML > 0) {
		$.ajax({
			type: "POST",
			url: "http://" + window.location.host + "/account/checkout/",
			data: $("#" + form.id).serialize(),
			error: function() {
				alert("Unable to checkout.\nPlease try again.")
			}
		});
	}
	
	return false;
}

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

		var allItemsCont = document.getElementById("all-items-cont");
		allItemsCont.innerHTML = "";
		
		$.ajax({
			'url': url,
			'success': function(data) {
				var json = JSON.parse(data);
				
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
					
					p.innerHTML += item.unitsAvailable;
					
					if (item.saleStart && item.saleEnd) {
						p = document.createElement("p");
						itemCont.appendChild(p);

						strong = document.createElement("strong");
						strong.innerHTML = "Sale Start: "
						p.appendChild(strong);
						
						p.innerHTML += item.saleStart + "<br>";

						strong = document.createElement("strong");
						strong.innerHTML = "Sale End: "
						p.appendChild(strong);
						
						p.innerHTML += item.saleEnd;
					}

					if (item.discountStart && item.discountEnd) {
						p = document.createElement("p");
						itemCont.appendChild(p);

						strong = document.createElement("strong");
						strong.innerHTML = "Discount Start: "
						p.appendChild(strong);
						
						p.innerHTML += item.discountStart + "<br>";

						strong = document.createElement("strong");
						strong.innerHTML = "Discount End: "
						p.appendChild(strong);
						
						p.innerHTML += item.discountEnd;
					}

					if (item.loggedIn) {
						var form = document.createElement("form");
						form.id = "add-to-cart-form-" + item.id;
						form.classList.add("inline");
						form.onsubmit = "return addToCart(this)";
						itemCont.appendChild(form);

						var csrf = document.createElement("input");
						csrf.type = "hidden";
						csrf.name = "csrfmiddlewaretoken";
						csrf.value = getCookie("csrftoken");
						form.appendChild(csrf);

						var input = document.createElement("input");
						input.type = "submit";
						input.classList.add("button");
						input.value = "Add to Cart";
						form.appendChild(input);
					}

					var hr = document.createElement("hr");
					itemCont.appendChild(hr);
				}
			},
			'error': function() {
				var h3 = document.createElement("h3");
				h3.classList.add("text-center");
				h3.innerHTML = "No Items Found";
				allItemsCont.appendChild(h3);
			}
		})
	}, 500);
}


function getCookie(cname)
{
	var name = cname + "=";
	var ca = document.cookie.split(";");

	for (var i = 0; i < ca.length; i++) {
		var c = ca[i];

		while (c.charAt(0) == " ") {
			c = c.substring(1);
		}

		if (c.indexOf(name) == 0) {
			return c.substring(name.length, c.length);
		}
	}

	return "";
}