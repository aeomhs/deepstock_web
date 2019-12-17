var chart = c3.generate({
   bindto: '#chart',
    data: {
       x: 'x',
       columns: [
           ['x', '2019-11-01', '2019-11-02', '2019-11-03', '2019-11-04', '2019-11-05', '2019-11-08'],
           ['price', 53000, 53300, 53400, 53100, 50800, 51900]
       ]
    },
    axis: {
        x: {
            type: 'timeseries',
            tick: {
                format: '%Y-%m-%d'
            }
        }
    }
});