function flashMessages(data){
    html = '';

    for (i = 0; i < data.length; i++) {
        html += `
        <div class="alert alert-${data[i]['type']}">
            <a href="#" class="close" data-dismiss="alert">&times;</a>
            ${data[i].message}
        </div>`;
    }
    return html;
};

function ajaxGetWithFlash(target_user, follow) {
    const Axios = window.axios;
    const endpoint = follow ? `/follow/${target_user}` : `/unfollow/${target_user}`;
    const flashBox = document.getElementById('flash');
    const followLink = document.getElementById('follow-link')
    const linkHTML = follow ? (
        `<button type="button" class="btn btn-info pt-1 pb-1 unfollow-button" onclick="unFollowUser('${target_user}')">
            Unfollow
        </button>`
    ) : (
        `<button type="button" class="btn btn-info pt-1 pb-1 follow-button" onclick="followUser('${target_user}')">
            Follow
        </button>`
    );

    console.log(followLink);
    console.log(linkHTML);

    Axios.get(endpoint).then((response) => {
        const messages = response.data.flash_messages;
        const redirect = response.data.redirect;

        if (redirect) {
            window.location.href = redirect;
        }

        followLink.innerHTML = linkHTML;
        if (flashBox) {
            flashBox.innerHTML = flashMessages(messages);
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