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

function toggleMore(index) {
    console.log("Toggle more called for index:", index);
    const message = document.getElementById('message-' + index);
    const moreBtn = message.nextElementSibling; // 버튼을 찾음

    // 펼쳐졌으면 숨기고, 숨겨졌으면 펼침
    if (message.style.maxHeight === 'none' || message.style.maxHeight === '') {
        console.log("Expanding message...");
        message.style.maxHeight = '4.8em'; // 3줄로 다시 축소
        message.style.overflow = 'hidden';
        message.style.textOverflow = 'ellipsis';
        moreBtn.innerText = '더보기';
    } else {
        console.log("Collapsing message...");
        message.style.maxHeight = 'none'; // 내용 펼침
        message.style.overflow = 'visible';
        message.style.textOverflow = 'clip';
        moreBtn.innerText = '닫기';
    }
}
