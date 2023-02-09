function fetch_data_MC() {
    var rows = []
    for (var i = 0; i < 5; i++) {
        rows.push({
            multipleChoice: '題目內容',
            maxScore: ~~(Math.random() * 10),
            MCAction: `
            <button class="btn btn-primary w-50 MCUpdate">編輯</button>
            <button class="btn btn-danger w-50 MCDelete">刪除</button>
            `
        })
    }
    return rows
}

$(document).ready(function () {
    $('#MCTable').bootstrapTable('load', fetch_data_MC())
})

function fetch_data_SA() {
    var rows = []
    for (var i = 0; i < 3; i++) {
        rows.push({
            shortAnswer: '題目內容',
            SAAction: `
            <button class="btn btn-primary w-50 SAUpdate">編輯</button>
            <button class="btn btn-danger w-50 SADelete">刪除</button>
            `
        })
    }
    return rows
}

$(document).ready(function () {
    $('#MCTable').bootstrapTable('load', fetch_data_MC())
    $('#SATable').bootstrapTable('load', fetch_data_SA())
})