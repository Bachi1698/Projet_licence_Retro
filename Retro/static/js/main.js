// rotate arrow 
var sidebarMenu = document.querySelectorAll(".sidebar-menu")

    sidebarMenu.forEach((menu) => {

    menu.addEventListener('click', function(e) {
        menu.childNodes[3].classList.toggle('fa-reverse');

            sidebarMenu.forEach(close =>{
                if(close != menu){
                    close.childNodes[3].classList.remove('fa-reverse');
            }
        })
    
    })
});

// inout type file
function bs_input_file() {
	$(".input-file").before(
		function() {
			if ( ! $(this).prev().hasClass('input-ghost') ) {
				var element = $("<input type='file' class='input-ghost' style='visibility:hidden; height:0'>");
				element.attr("name",$(this).attr("name"));
				element.change(function(){
					element.next(element).find('input').val((element.val()).split('\\').pop());
				});
				$(this).find("button.btn-choose").click(function(){
					element.click();
				});
				$(this).find("button.btn-reset").click(function(){
					element.val(null);
					$(this).parents(".input-file").find('input').val('');
				});
				$(this).find('input').css("cursor","pointer");
				$(this).find('input').mousedown(function() {
					$(this).parents('.input-file').prev().click();
					return false;
				});
				return element;
			}
		}
	);
}
$(function() {
	bs_input_file();
});

/* menu de navigation */
var open = document.querySelector('.icone');
var close = document.querySelector('.iconeClose');
var sidebar = document.querySelector('.sidebar-main');

open.addEventListener('click', function(e){
    e.stopPropagation();
    sidebar.classList.add('active')
})

close.addEventListener('click', function(e){
    e.stopPropagation();
    sidebar.classList.remove('active')
})