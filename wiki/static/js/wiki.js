function viewPageMain () { }
function editPageMain () {
    const baseURL = location.origin + location.pathname;
    const contentEditor = document.querySelector('#post-editor-content');
    const previewArea = document.querySelector('#post-preview');


    const submitBtn = document.querySelector('#submit-content');
    submitBtn.addEventListener('click', () => {
        const pageKey = document.querySelector('#post-name').value;
        const title = document.querySelector('#title-editor').value;
        const queryBody = JSON.stringify({ title: title, article: pageKey, markdown: contentEditor.value });
        fetch(baseURL + '/submit', {
            method: 'POST',
            body: queryBody
        }).then(response => {
            if (!response.ok) {
                throw new Error('通信に失敗しました');
            }
            return response.json();
        }).then(json => {
            location.href = json.redirect;
        });
    });

    const previewBtn = document.querySelector('#preview-content');
    previewBtn.addEventListener('click', () => {
        const queryBody = JSON.stringify({ title: 'title', markdown: contentEditor.value });
        fetch(baseURL + '/preview', {
            method: 'POST',
            body: queryBody
        }).then(response => {
            if (!response.ok) {
                throw new Error('通信に失敗しました');
            }
            return response.json();
        }).then(json => {
            previewArea.innerHTML = json.content;
        });
    });

    const ignoreBtn = document.querySelector('#ignore-change');
    ignoreBtn.addEventListener('click', () => {
        location.href = location.origin + location.pathname + location.search.split('&')[0];
    });
}


function onLoad () {
    const isEdit = !!document.querySelector('#post-editor');
    (isEdit ? editPageMain : viewPageMain)();
}

window.addEventListener('load', onLoad);
