import axios from 'axios';

import {dict_to_xy_arr, getIsoDateString} from "../../../utils";

function getDateString(timeslice) {
    let date = new Date();
    let dateString = "&start_date=";

    switch (timeslice) {
        case "hour":
            date.setHours(date.getHours() - 12);
            break;
        case "day":
            date.setDate(date.getDate() - 7);
            break;
        case "week":
            date.setDate(date.getDate() - 56);
            date.setDate(date.getDate() - date.getDay() + 1);
            break;
        case "month":
            date.setMonth(date.getMonth() - 12);
            date.setDate(1);
            console.log("calculated date: ", date);
            break;
        case "year":
            console.log("current year: ", date.getFullYear());
            date.setYear(date.getFullYear() - 5);
            date.setMonth(0);
            date.setDate(1);
            console.log("calculated date: ", date);
            break;       
        default:
            break;
    }

    dateString = dateString + getIsoDateString(date);

    if (timeslice === "all_time") {
        dateString = "";
    }

    return dateString;
}

// function getGranularity(timeslice) {
//     switch (timeslice) {
//     case "hour":
//         return "minute";
//     case "day":
//         return "hour";
//     case "week":
//         return "day";
//     case "month":
//         return "day";
//     case "year":
//         return "month";
//     default:
//         return "day";
//     }
// }

async function requestStatisticData(dashboard_id, statistic, timeslice, callback) {
    let dateString = getDateString(timeslice);
    return await axios({
        method: 'get',
        withCredentials: true,
        url: window.api_path + '/api/dashboards/' + dashboard_id + '/statistic?statistic=' + statistic + '&timeslice=' + timeslice + dateString + '&timeslice_is_static=True',
    }).then((response) => {
        console.log("Statistics data returned: ", response);
        const timeslice_statistics_data = dict_to_xy_arr(response.data);
        console.log("timeslice_statistics_data", statistic, timeslice_statistics_data);
        callback(timeslice_statistics_data);
    }).catch((error) => {
        console.log('error while fetching dashboard statistics data', error);
    });
}


export {requestStatisticData};
