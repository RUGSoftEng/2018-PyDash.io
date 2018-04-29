/*
This file contains small functions that do not belong elsewhere.

If things grow, they should move to their own module, of course.
*/


// Transforms a hashmap of key-value pairs into an array of {x: key, y: value} objects.
function dict_to_xy_arr(dict){
    let res =  Object.entries(dict).map(function([key, value]){
        return {x: key, y: value};
    });
    return res;
}

export {dict_to_xy_arr};
