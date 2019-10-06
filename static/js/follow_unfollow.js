function flashMessages(data){
    let html = '';

    for (let i = 0; i < data.length; i++) {
        html += `
        <div class="alert alert-${data[i]['type']}">
            <a href="#" class="close" data-dismiss="alert">&times;</a>
            ${data[i].message}
        </div>`;
    }
    return html;
}

function ajaxGetWithFlash(target_user, follow) {
    const endpoint = follow ? `/follow/${target_user}` : `/unfollow/${target_user}`;
    const buttonTxt = follow ? "Unfollow" : "Follow";
    const Axios = window.axios;

    const linkHTML = 
        `<button data-follow="${!follow}" data-user="${target_user}" class="btn btn-info pt-1 pb-1">
            ${buttonTxt}
        </button>`;

    Axios.get(endpoint).then((response) => {
        const messages = response.data['flash_messages'];
        const flashBox = $('#flash');
        const followLinks = $('.follow-link');
        const popover = $('.popover');

        followLinks.each((index, _this) => {
            _this.innerHTML = linkHTML;
        });
        if (flashBox) {
            flashBox.html(flashMessages(messages))
        }
        
        if (popover) {
            popover.remove();
        }
    }).catch((error) => {
        console.error(`Error: ${error}, please contact the administrator`);
    });
}

function unFollowUser(target_user) {
    ajaxGetWithFlash(target_user, false)
}

function followUser(target_user) {
    ajaxGetWithFlash(target_user, true)
}

$(function() {
    $('body').on('click', '.follow-link .btn', (e) => {
        e.preventDefault();

        const link = $('.follow-link .btn');
        const follow = link.data('follow');
        const target_user = link.data('user');

        if (follow) {
            followUser(target_user);
        } else {
            unFollowUser(target_user);
        }
    })
});
