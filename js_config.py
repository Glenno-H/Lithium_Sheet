from st_aggrid import JsCode


sparkline_config = {
    "sparklineOptions": {"type": "bar", "valueAxisDomain": [0, 20],
                        "paddingOuter": 0,
                         },
}
sparkline_params = \
    JsCode("""
    function(params) {
        return {sparklineOptions: {type: "bar", valueAxisDomain: [0.0, 100.0]}},
    }
    """)

sparkline_data = \
    JsCode("""
    function(params) {
        return [parseInt(params.data.CostPerAH)];
    }
    """)

show_notes = \
    JsCode("""
    function(params) {
    let myWin = window.open("Topic", "wid", "toolbar=no,menubar=no,location=no,status=no,height=285,width=500, left=450, top=175");
    myWin.document.write("<span style='font-size: 20px; color:black;'>" + params.data.Notes + "</span>");
    myWin.focus();
    }
    """)

brand_cell_renderer = \
    JsCode("""
    function(params) {
    return `<a href=${params.data.URL} target="_blank">${params.data.Brand}</a>`
    }
    """)

url_cell_renderer = \
    JsCode("""
    function(params) {
    return `<a href=${params.data.URL} target="_blank">${params.data.URL}</a>`
    }
    """)

celsius_formatter = \
    JsCode("""
    function(params) {
    return `${params.value}c`
    }
    """)

weight_formatter = \
    JsCode("""
    function(params) {
    return `${params.value}kg`
    }
    """)