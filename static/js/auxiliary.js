function request(method, url, data) {
    return new Promise((resolve, reject) => {
        let loadHtml = '<div id="load"><div style="top: 0;right: 0;bottom: 0;left: 0;z-index: 8192;position: fixed;background: rgba(0,0,0,.4);backdrop-filter: blur(7px)"></div><div style="position: fixed;right: 0;left: 0;z-index: 8192;margin: auto;background-color: #fff;border-radius: 12px;-webkit-box-shadow: 0 11px 15px -7px rgb(0 0 0 / 20%), 0 24px 38px 3px rgb(0 0 0 / 14%), 0 9px 46px 8px rgb(0 0 0 / 12%);display: block;top: 0;bottom: 0;left: 0;height: 145px;width: 220px"><div style="height: 18px"></div><div style="display: flex;align-items: center;flex-direction: column"><style>@keyframes spin{0%{transform:rotate(0deg)}100%{transform:rotate(360deg)}}</style><div style="width: 48px;height: 48px;border: 16px solid #f3f3f3;border-top: 16px solid #3f51b5;border-radius: 100%;animation: spin 1s linear infinite"></div></div><div style="height: 12px;"></div><div style="text-align: center;color: #3f51b5;font-weight: 600;font-size: 18px">加载中</div></div></div>';
        let loadElement = document.createElement('div');
        loadElement.innerHTML = loadHtml;
        document.body.appendChild(loadElement);

        axios({
            method: method,
            url: url,
            params: method === 'get' ? data : null,
            data: method === 'post' ? data : null,
        }).then((response) => {
            loadElement.remove();
            if (response.data.code === 200) {
                resolve(response);
            } else {
                mdui.alert(response.data.message);
            }
        }).catch((response) => {
            loadElement.remove();
            mdui.snackbar({message: '请求失败'});
        });
    });
}

function copyText(text) {
    let dummy = document.createElement('textarea');
    document.body.appendChild(dummy);
    dummy.value = text;
    dummy.select();
    document.execCommand('copy');
    document.body.removeChild(dummy);
}

function analysisShortUrl(url) {
    let re = /^((https?:)?\/\/)?([^\/\s]+)(\/\S*)?$/;
    let matches = url.trim().match(re);
    let domain = matches[3];
    let signature = matches[4] ? matches[4].substr(1) : '';
    return {domain, signature};
}

function timestampToTime(timestamp) {
    let date = new Date(timestamp * 1000),
    Y = date.getFullYear() + '-',
    M = (date.getMonth() + 1 < 10 ? '0' + (date.getMonth() + 1) : date.getMonth() + 1) + '-',
    D = date.getDate() + ' ',
    h = date.getHours() + ':',
    m = date.getMinutes() + ':',
    s = date.getSeconds();
    return Y + M + D + h + m + s;
}