// Get the data from the blood_type_info data attribute
var bloodData = [];
var bloodLabels = [];
var bloodColors = [];
var blood_type_doc = document.querySelector('#myChart');
var blood_type_data = blood_type_doc.datasets.bloodInfo;
// var bloodTypeData = JSON.parse(document.getElementById('myChart').getAttribute('data-blood-info'));
var bloodTypeData = JSON.parse(blood_type_data);
for (var i = 0; i < bloodTypeData.length; i++) {
    bloodData.push(Number(bloodTypeData[i]['available_quantity']));
    bloodLabels.push(bloodTypeData[i]['blood_type']);
    bloodColors.push('#' + Math.floor(Math.random() * 16777215).toString(16)); // generate a random color for each blood type
}

// Create the pie chart
var ctx = document.getElementById('myChart').getContext('2d');
var myChart = new Chart(ctx, {
    type: 'pie',
    data: {
        labels: bloodLabels,
        datasets: [{
            data: bloodData,
            backgroundColor: bloodColors,
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        title: {
            display: true,
            text: 'Blood Type Distribution'
        }
    }
});



// // Get the data from the blood_type_info data attribute
// var bloodData = [];
// var bloodLabels = [];
// var bloodColors = [];
// var bloodTypeData = JSON.parse(document.getElementById('myChart').getAttribute('data-blood-info'));
// for (var i = 0; i < bloodTypeData.length; i++) {
//     bloodData.push(bloodTypeData[i]['available_quantity']);
//     bloodLabels.push(bloodTypeData[i]['blood_type']);
//     bloodColors.push('#' + Math.floor(Math.random() * 16777215).toString(16)); // generate a random color for each blood type
// }

// // Create the pie chart
// var ctx = document.getElementById('myChart').getContext('2d');
// var myChart = new Chart(ctx, {
//     type: 'pie',
//     data: {
//         labels: bloodLabels,
//         datasets: [{
//             data: bloodData,
//             backgroundColor: bloodColors,
//         }]
//     },
//     options: {
//         responsive: true,
//         maintainAspectRatio: false,
//         title: {
//             display: true,
//             text: 'Blood Type Distribution'
//         }
//     }
// });