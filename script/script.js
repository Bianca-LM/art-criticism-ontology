function showResult(element) {
    element.style.backgroundColor = "rgb(236, 65, 8)"
    id = element.getAttribute('id')
    if (id == 'query-1') {
        result = document.getElementById('result-1')
        result.removeAttribute('class')
    }
    if (id == 'query-2') {
        result = document.getElementById('result-2')
        result.removeAttribute('class')
    }
    if (id == 'query-3') {
        result = document.getElementById('result-3')
        result.removeAttribute('class')
    }
    if (id == 'query-4') {
        result = document.getElementById('result-4')
        result.removeAttribute('class')
    }
    if (id == 'query-5') {
        result = document.getElementById('result-5')
        result.removeAttribute('class')
    }
}