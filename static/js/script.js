function deleteLetter(id) {
    if (confirm("정말로 이 편지를 삭제하시겠습니까?")) {
        // Fetch로 DELETE 요청 보내기
        fetch(`/delete/${id}`, {
            method: 'DELETE',
        })
        .then(response => {
            if (response.ok) {
                alert("편지가 삭제되었습니다!");

                // 삭제된 편지를 DOM에서 즉시 제거
                const letterItem = document.getElementById(`letter-${id}`);
                if (letterItem) {
                    letterItem.remove(); // DOM에서 해당 편지 항목 제거
                }
            } else {
                alert("편지를 삭제하는데 문제가 발생했습니다.");
            }
        })
        .catch(error => {
            console.error("Error:", error);
            alert("오류가 발생했습니다. 다시 시도해주세요.");
        });
    }
}



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

