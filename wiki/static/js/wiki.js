const baseURL = location.origin + location.pathname;
function viewPageMain () { }
function editPageMain () {
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

    const imageGalleryBtn = document.querySelector('#insert-image-button');
    imageGalleryBtn.addEventListener('click', () => {
        const imageGalleryURL = location.origin + location.pathname + '?page=image-gallery';
        window.open(imageGalleryURL, '_blank');
    });

    const controllers = document.querySelectorAll('#post-content-controller button');
    controllers.forEach(btn => {
        btn.addEventListener('mouseover', () => {
            btn.classList.add('open');
        });
        btn.addEventListener('mouseleave', () => {
            btn.classList.remove('open');
        });
    });
}

function imageGalleryPageMain () {
    const imageAPIURL = baseURL + '/image';
    const fileNameForm = document.querySelector('#image-filename');
    const fileDeleteBtn = document.querySelector('#delete-image-button');
    const markdownForm = document.querySelector('#image-markdown-text');
    const markdonwCopyBtn = document.querySelector('#copy-markdown-button');
    const uploadFileForm = document.querySelector('#new-image-select');
    const uploadSubmitBtn = document.querySelector('#upload-image-button');
    const imageGalleryList = document.querySelector('#image-gallery-list');
    const imageGalleryCards = imageGalleryList.querySelectorAll('.image-gallery-card');

    fileDeleteBtn.addEventListener('click', () => {
        const filename = fileNameForm.value;
        if (filename.length == 0) {
            return;
        }
        if (!confirm(`${filename} を削除します。`)) {
            return;
        }
        const queryBody = JSON.stringify({ filename: filename });
        fetch(imageAPIURL + '/delete', {
            method: 'POST',
            body: queryBody
        }).then(response => {
            if (!response.ok) {
                throw new Error('通信に失敗しました');
            }
            location.reload();
        });
    });

    markdownForm.addEventListener('click', () => {
        markdownForm.select();
    });

    markdonwCopyBtn.addEventListener('click', () => {
        if (markdownForm.value.length == 0) {
            return;
        }

        markdownForm.select();
        document.execCommand("copy"); // TODO: Not recommended way
    });

    imageGalleryCards.forEach(elm => {
        elm.addEventListener('click', () => {
            const filename = elm.querySelector('figcaption').textContent;
            fileNameForm.value = filename;
            const markdownCopyText = `![](${filename} "")`;
            markdownForm.value = markdownCopyText;
            uploadFileForm.value = '';
        });
    });

    uploadFileForm.addEventListener('change', () => {
        const filename = uploadFileForm.value.replace(/^.*[\\\/]/, '');
        fileNameForm.value = filename;
        markdownForm.value = '';
    });

    uploadSubmitBtn.addEventListener('click', () => {
        if (uploadFileForm.files.length == 0) {
            fileNameForm.value = '';
            markdownForm.value = '';
            return;
        }
        const filename = uploadFileForm.value.replace(/^.*[\\\/]/, '');
        const sendFile = uploadFileForm.files[0];

        const formData = new FormData();
        formData.append('image', sendFile);
        formData.append('filename', filename);
        fetch(imageAPIURL + '/add', {
            method: 'POST',
            body: formData
        }).then(response => {
            if (!response.ok) {
                throw new Error('通信に失敗しました');
            }
            return response.json();
        }).then(json => {
            const err = json.error;
            if (err === undefined) {
                location.reload();
            } else if (err === 'FileExist') {
                alert('ファイル名が重複します。\nファイル名を変更してください。');
            }
            return;
        });
    });
}

function onLoad () {
    const isEdit = !!document.querySelector('#post-editor');
    const isImageGallery = !!document.querySelector('#image-gallery-panel');

    if (isEdit) {
        editPageMain();
    } else if (isImageGallery) {
        imageGalleryPageMain();
    } else {
        viewPageMain();
    }
}

window.addEventListener('load', onLoad);
