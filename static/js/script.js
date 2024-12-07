function changeRows() {
    const letterList = document.querySelector('.letter-list');
    const selectedRows = document.getElementById('rows').value;

    // 기존 클래스 제거
    letterList.classList.remove('one-row', 'two-rows', 'three-rows', 'four-rows');

    // 새 클래스 추가
    if (selectedRows === '1') {
        letterList.classList.add('one-row');
    } else if (selectedRows === '2') {
        letterList.classList.add('two-rows');
    } else if (selectedRows === '3') {
        letterList.classList.add('three-rows');
    } else if (selectedRows === '4') {
        letterList.classList.add('four-rows');
    }
}


