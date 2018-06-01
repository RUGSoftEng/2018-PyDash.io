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

// Returns a string containing the date, contained in the Date object passed to the function, according to ISO standards.
function getIsoDateString(date) {
    let year, month, dt, string;
    year = date.getFullYear();
    month = date.getMonth()+1;
    dt = date.getDate();

    if (dt < 10) {
        dt = '0' + dt;
    }
    if (month < 10) {
        month = '0' + month;
    }

    string = year+'-'+month+'-'+dt;
    return string;
}

// Converts the data returned from the backend into a usable format for a Nivo heatmap.
function convertHeatmapData(data) {
    let dayCount = data.length;
    let currentDate = new Date();
    let heatmap = [];
    for (let day in data) {
        let dayData = {};
        let calculatedDate = new Date();
        calculatedDate.setDate(currentDate.getDate() - (dayCount-day));
        dayData["date"] = getIsoDateString(calculatedDate);

        for (let hour = 0; hour < 24; hour++) {
            let key = '';
            if (hour < 10) {
                key = '0' + hour + ':00';
            } else {
                key = '' + hour + ':00';
            }
            dayData[key] = data[day][hour];
        }

        heatmap.push(dayData);
    }
    return heatmap;
}

export {dict_to_xy_arr, api_to_bar_data, getIsoDateString, convertHeatmapData};
