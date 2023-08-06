$( document ).ready(function() {
  // Replace any fa-icon roles
  $('.fa-icon').each(function(){$(this).html('<i class="fa ' + $(this).html() + '" aria-hidden="true"></i>')})
  ////////////////
  // Mobile TOC//
  ///////////////

  // Mobile global TOC
  $('<div class="g-menu-btn" id="g-menu-btn"><i id="g-closedMenu" class="fa fa-bars" aria-hidden="true"></i><i id="g-openMenu" class="fa fa-times" aria-hidden="true" style="display: none;"></i>   </div>').insertAfter('.toctree-l1.current>a')
  $('.g-menu-btn').click(function(){
    if ($('.g-menu-btn').siblings('ul').hasClass('expand')){
          $('.g-menu-btn').siblings('ul').removeClass('expand');
          $('.g-menu-btn').siblings('ul').slideToggle(300)
          $('#g-closedMenu').show()
          $('#g-openMenu').hide()
                        } else {
          $('.g-menu-btn').siblings('ul').addClass('expand');
          $('.g-menu-btn').siblings('ul').slideToggle(300)
          $('#g-closedMenu').hide()
          $('#g-openMenu').show()
        }
    })
  // Mobile local TOC
  $('#menu').children().slideToggle(0);
  $('#openMenu').hide()
  $('.menu-btn').click(function(){
    if ($('#menu').hasClass('expand')){
          $('#menu').removeClass('expand');
          $('#menu').children().slideToggle(300);
          $('#closedMenu').show()
          $('#openMenu').hide()
                        } else {
          $('#menu').addClass('expand');
          $('#menu').children().slideToggle(300);
          $('#closedMenu').hide()
          $('#openMenu').show()
        }
      })
  // Hide empty TOCs on desktop
  if ($('ul.current > li > ul').children().length == 0) {
    $('ul.current > li > ul').hide();
  }
  // Hide empty mobile global TOC if no children
  if ($('ul.current').children().length == 0){
    $('.g-menu-btn').hide();
  }
  // Hide empty mobile slider menus
  if ($('#menu > ul > li').children().length == 1) {
    $('#menu > ul > li').hide();
    $('#menu-btn').hide();
  }

  // Constructors
  $('.property').siblings('.descclassname').show()
  $('.property').hide()

  /////////////////////////
  // Expandable sections //
  /////////////////////////

  // Check for collapsible signaler
  $(':header:contains("[[]]")').html(function (i, t) {
    $(this).addClass('collapsible');
    return t.replace('[[]]', '<span class="hidden"> </span>');
  })
  $('.collapsible').addClass('collapsed');
  $('.collapsible').attr('aria-expanded','false')
  $('.collapsible').siblings().slideToggle(0);
  // Remove signaler from references—toc and in main
  $('.reference:contains("[[]]")').html(function (i, t) {
    return t.replace('[[]]', '<span class="hidden"> </span>');
  })

  // Make it clickable
  $('.collapsible').click( function() {
    if ($(this).hasClass('collapsed')){
      $(this).removeClass('collapsed');
      $(this).attr('aria-expanded','true')
      $(this).siblings().slideToggle(300);
      $("span[id]").attr('style','display: none;')
      $(this).siblings().not('span').wrapAll('<div class="colsection"></div>');
      $(this).after($(this).siblings(".colsection"));
    } else {
      $(this).addClass('collapsed');
      $(this).attr('aria-expanded','false')
      $(this).siblings('.colsection').children().slideToggle(300);
      $("span[id]").attr('style','display: none;')
      $(this).siblings('.colsection').children().unwrap();
    }
  });
  // Keyboard navigation for collapsible sections
  $(".collapsible").attr("tabindex", "0");
  $(".collapsible").on("keydown", function(e){
    if(e.which === 13){
      $(this).trigger("click");
    }
  });
  // Unhide section if user is referred its anchor
  function unhideCollapsed()
  {
    try {
    var anchorName = document.location.hash.substring(1);
    var collapsedAnchor = $("[id=" + anchorName + "]").children(".collapsed");
    $(collapsedAnchor).removeClass('collapsed');
    $(collapsedAnchor).attr('aria-expanded','true');
    $(collapsedAnchor).siblings().slideToggle(300);
    $("span[id]").attr('style','display: none;');
    $(collapsedAnchor).siblings().wrapAll('<div class="colsection"></div>');
    $(collapsedAnchor).after($(collapsedAnchor).siblings(".colsection"));
    } catch (e) {}
    try {
      var anchorName = document.location.hash.substring(1);
      var collapsedAnchor = $("[id=" + anchorName + "]").siblings(".collapsed");
      $(collapsedAnchor).removeClass('collapsed');
      $(collapsedAnchor).attr('aria-expanded','true');
      $(collapsedAnchor).siblings().slideToggle(300);
      $("span[id]").attr('style','display: none;');
      $(collapsedAnchor).siblings().wrapAll('<div class="colsection"></div>');
      $(collapsedAnchor).after($(collapsedAnchor).siblings(".colsection"));
    } catch (e) {}
  }
  unhideCollapsed();
  // Unhide section if user changes hash in page
  $(window).on('hashchange', function(e){
   unhideCollapsed();
  });

  //////////////////////////
  // Guides dropdown menu //
  //////////////////////////

  $(".dropdown").on("keydown", function(e){
    if(e.which === 13){
      $(this).toggleClass("showdrop");
      $('.sub-menu').attr("aria-hidden", function(index, attr) {return attr == "true" ? "false" : "true"});
      $('.sub-menu', this).toggle();
    }
  });
  // Guides dropdown
  $("li.dropdown").hover(function() {
    $(this).addClass("showdrop")
    $('.sub-menu').attr("aria-hidden", "false")
    $(".sub-menu").show();
  }, function() {
    $('.sub-menu').attr("aria-hidden", "true")
    $(this).removeClass("showdrop");
    $(".sub-menu").hide()
  });

})

// Additional functions
function expandAll (){
  $('.collapsible').siblings('.colsection').children().unwrap();
  $('.collapsible').siblings().slideDown(300);
  $('.collapsible').removeClass('collapsed');
  $('.collapsible').attr('aria-expanded','true')
  $('.collapsible').each(function addColSecAll(){$(this).siblings().wrapAll('<div class="colsection"></div>')});
}
function collapseAll (){
  $('.collapsible').siblings('.colsection').children().slideToggle(300);
  $("span[id]").attr('style','display: none;')
  $('.collapsible').siblings('.colsection').children().unwrap();
  $('.collapsible').addClass('collapsed');
  $('.collapsible').attr('aria-expanded','false')
}