function draw_chart(stock_name, date_list, price_list) {
    let dates = ['x'].concat(date_list)
    let prices = [stock_name].concat(price_list)

    let chart = c3.generate({
        bindto: '#chart',
        data: {
            x: 'x',
            columns: [
                dates,
                prices
            ]
        },
        axis: {
            x: {
                type: 'timeseries',
                tick: {
                    format: '%m-%d'
                }
            }
        }
    });
}