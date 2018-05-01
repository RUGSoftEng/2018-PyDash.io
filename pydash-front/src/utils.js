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

// Transforms the returned endpoint data from the api into a form that can be
// displayed in a nivo bar graph.
function api_to_bar_data(endpoints) {
    let res = [];
    for (let i in endpoints) {
      let name = endpoints[i].name;
      let average_execution_time = endpoints[i].aggregates.average_execution_time;
      res.push({'name': name, 'average_execution_time': average_execution_time});
    }
    console.log('bar data', res);
    console.log('length: ' + res.length);
    return res;
}

export {dict_to_xy_arr, api_to_bar_data};
