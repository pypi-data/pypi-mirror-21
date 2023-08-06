"use stric";
/**
 * Convert string to boolean in a dict recursively
 *
 * @param      {<type>}  config  The configuration
 */
var searchBoolean = function(stoneConfig){
    $.each(stoneConfig, function(key, value){
        if(typeof(value)=='object'){
            if(typeof(value.includes)=='undefined'){
                // DICCIONARIO
                if (Object.keys(stoneConfig).includes(key)){
                    stoneConfig[key] = searchBoolean(stoneConfig[key])
                }
            }else{
                // LISTA
            }
        }
        else{
            if(value=='true' || value == 'false'){ stoneConfig[key]=value=='true'}
        }
    })
    return stoneConfig
}

/**
 * Extend a dict recursively
 *
 * @param      {<dict>}  first_object    Default confing
 * @param      {<dict>}  second_objects  Custom config
 * @return     {<dict>}  config merged
 */
var extendJqueryExtend = function(first_object, second_objects){
    $.each(first_object, function(key, value){
        if(typeof(value)=='object'){
            if(typeof(value.includes)=='undefined'){
                // DICCIONARIO
                if (Object.keys(second_objects).includes(key)){
                    first_object[key] = jQuery.extend(first_object[key], second_objects[key])
                }
            }else{
                // LISTA
            }
        }
    })
    return jQuery.extend(first_object, second_objects)
}