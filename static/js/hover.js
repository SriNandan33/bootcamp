const Axios = window.axios;

const popoverConfig = (element, data) => {
    return {
        trigger: 'manual',
        html: true,
        animation: false,
        container: element,
        content: data,
    }
};

$(function () {
    let timer = null;
    let xhr;
    const userPopup = $('.user_popup');

    userPopup.on('mouseenter', (event) => {
        let element = $(event.currentTarget);
        const username = element.first().text().trim();
        xhr = Axios.CancelToken.source();

        timer = setTimeout(() => {
            Axios.get(`/user/${username}/popup`, {
                cancelToken: xhr.token
            }).then((response) => {
                const config = popoverConfig(element, response.data);
                element.popover({...config}).popover('show');
            }).catch(error => console.error(error));
        }, 1000)
    });

    userPopup.on('mouseleave', (event) => {
        let element = $(event.currentTarget);

        if (timer) {
            clearTimeout(timer);
            timer = null;
        }

        if (xhr) {
            xhr.cancel('');
        }

        element.popover('dispose');
    });
});