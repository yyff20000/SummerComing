/*!
 * SmartClass Checkbox plugin
 * ===================================
 *
 * developed by Mert Simsek (simsek97@gmail.com)
 * for SmartClass Project [www.smartclass.us]
 * -------------------------
 * @usage $("#element").simsCheckbox();
 */
 
(function($) {

    //vars
    var _mobile = /ipad|iphone|ipod|android|blackberry|windows phone|opera mini|silk/i.test(navigator.userAgent);

    //plugin init
    $.fn.simsCheckbox = function(options) {
    
        var selectorElt = this,
            checkboxClass = "btn btn-block btn-social";
    
        //settings
        var settings = $.extend({
    
            //style
            //set treat as checkbox or radio
            btnStyle: 'checkbox',
            
            //selector height
            height: 'auto',
            
            //element
            element: "li",
        
            //title icon
            titleIcon: "square-o",
    
            //unchecked class
            uncheckedClass: "btn-default",
        
            //checked class
            checkedClass: "btn-warning",
            
            //select/unselect all button
            selectAllBtn: false,
    
            //select/unselect text
            selectAllText: 'Select/Unselect All',
            
            //callback fn ifChecked
            ifChecked: function() {},

            //callback fn ifUnChecked
            ifUnChecked: function() {},

            //callback fn ifToggled
            ifToggled: function() {},
    
        }, options);

        return selectorElt.each(function(){
      
            //set some css for the selector
            selectorElt.css({'margin': '0', 'padding': '0'});
            
            //set the height of the selector first
            if(settings.height == 'auto') selectorElt.css('height', 'auto');
            else selectorElt.css({'height': settings.height, 'overflow': 'auto'});
        
            //add an identifier class to the elements
            selectorElt.find(settings.element).addClass('sims-selectable');
            
            //get elements and handle
            selectorElt.find(settings.element).each(function(i) {
              
                var simsElement=$(this), simsElementTitle=simsElement.html();
                
                //add checkbox class
                simsElement.addClass(checkboxClass);
                
                //add checked or unchecked class
                if(simsElement.hasClass('checked')) simsElement.addClass(settings.checkedClass).html('<i class="fa fa-fw fa-check-' + settings.titleIcon + '"></i> ' + simsElementTitle);
                else simsElement.addClass(settings.uncheckedClass).html('<i class="fa fa-fw fa-' + settings.titleIcon + '"></i> ' + simsElementTitle);
                
                //set click event if it is not disabled
                simsElement.off('click').on('click', function (e) {
    
                    e.preventDefault();
                    
                    //if the element is disabled then do nothing
                    if($(this).hasClass('disabled')) return false;
                    
                    //if the style is radio kind then unselect all first
                    if(settings.btnStyle == 'radio')
                    {
                        selectorElt.find(settings.element).addClass(settings.uncheckedClass).removeClass(settings.checkedClass).find('i').addClass('fa-' + settings.titleIcon).removeClass('fa-check-' + settings.titleIcon);
                    }
                    
                    //toggle the item
                    $(this).toggleClass(settings.uncheckedClass).toggleClass(settings.checkedClass).find('i').toggleClass('fa-' + settings.titleIcon).toggleClass('fa-check-' + settings.titleIcon);

                    //callback
                    clickCheckbox($(this));
                    
                }); //end simsElement click
              
            }); //end selectorElt each
            
            //set checkAll button
            if(settings.selectAllBtn)
            {
              
                //test all checked or not
                var allChecked = (selectorElt.find(settings.element).length == selectorElt.find(settings.element + '.checked').length) ? true : false;
                var selectAllBtnContainer = $( '<ul></ul>' ).css({'margin': '5px 0 0 0', 'padding': '0'});
                var selectAllBtnElt = $( '<' + settings.element +  ' class="sims-btn-select-all"></' + settings.element + '>' ).css('border', '1px dashed').addClass(checkboxClass + ' ' + (allChecked ? settings.checkedClass : settings.uncheckedClass)).html('<i class="fa fa-fw fa-' + (allChecked ? 'check-' : '') + settings.titleIcon + '"></i> '  + settings.selectAllText);
                
                selectorElt.after( selectAllBtnContainer.append(selectAllBtnElt) );
                
                //set click event for the selectAll button
                selectAllBtnContainer.find('.sims-btn-select-all').off('click').on('click', function (e) {
                    
                    //prevent default events
                    e.preventDefault();
                    
                    //get button
                    var thisButton = $(this);
                    
                    //toggle the item
                    thisButton.toggleClass(settings.uncheckedClass).toggleClass(settings.checkedClass).find('i').toggleClass('fa-' + settings.titleIcon).toggleClass('fa-check-' + settings.titleIcon);
                    
                    //if all items are selected then select-all button is checked
                    //if one of the items is unselected then select-all button is unchecked
                    selectorElt.find(settings.element + '.sims-selectable:not(.disabled)').each(function(){
                        
                        //fix classes of the items
                        if( thisButton.hasClass("btn-default") ) $(this).removeClass(settings.uncheckedClass).addClass(settings.checkedClass).find('i').removeClass('fa-' + settings.titleIcon).addClass('fa-check-' + settings.titleIcon);
                        else $(this).addClass(settings.uncheckedClass).removeClass(settings.checkedClass).find('i').addClass('fa-' + settings.titleIcon).removeClass('fa-check-' + settings.titleIcon);
                        
                        //trigger click event for the items
                        $(this).trigger("click");
                    
                    });
                
                });
              
            } //end if
        
            function clickCheckbox(item) {
                
                //check if the button checked or unchecked
                //then call function properly
                if(item.hasClass(settings.checkedClass)) settings.ifChecked.call(item);
                else settings.ifUnChecked.call(item);
                
                //call toggle function anyways
                settings.ifToggled.call(item);
                
            }
            
        }); //end return
        
    } //end function
    
}(jQuery));
