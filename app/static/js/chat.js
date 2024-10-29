let selectedUserId = null;
let socket = null;
let messagePollingInterval = null;
let messageInput = $('#message-input');
let sendBtn = $('#send-btn');
let messagesContainer = $('.chat-messages');


async function logout() {
    const result = await axios.post('/auth/logout/', {withCredentials: true});
    if (result && result.status === 200) {
        window.location.replace('/');
    } else {
        console.error(`Logout failed`);
    }
}

async function selectUser(userId, username) {
    selectedUserId = userId
    $('#username').text(username);
    messageInput.prop('disabled', false);
    messagesContainer.scrollTop(messagesContainer.prop('scrollHeight'));
    sendBtn.prop('disabled', false);
    $('#no-interlocutor').attr('hidden', true);
    await loadMessages(selectedUserId);
    connectWebsocket();
    startMessagePolling(selectedUserId);
}

async function loadMessages(userId) {
    try {
        const result = await axios.get(`/messages/${userId}`);
        messagesContainer.html(
            result.data.map((message) => createMessageElement(message.content, message.recipient_id, message.created_at)).join('')
        )
    } catch (error) {
        console.error(error);
    }
}


function connectWebsocket() {
    if (socket) socket.close();

    socket = new WebSocket(`ws://${window.location.host}/ws/${selectedUserId}`);
    socket.onopen = () => console.log('Connected');
    socket.onmessage = (event) => {
        const message = JSON.parse(event.data);
        if (message.recipient_id === selectedUserId) {
            addMessage(message.content, message.recipient_id, message.created_at);
        }

    };
    socket.onclose = () => console.log('Disconnected');
}

async function sendMessage() {
    const message = messageInput.val().trim();
    if (message && selectedUserId) {
        const data = {
            recipient_id: selectedUserId,
            content: message
        };

        try {
            axios.post('/messages/', data);
            socket.send(JSON.stringify(data));
            messageInput.val('');
        } catch (error) {
            console.error(error);
        }
    }
}

function addMessage(content, recipientId, createdAt) {
    const messageElement = createMessageElement(content, recipientId, createdAt);
    messagesContainer.append(messageElement);
    requestAnimationFrame(() => {
        messagesContainer.scrollTop(messagesContainer.prop('scrollHeight'));
    });
}

function createMessageElement(content, recipientId, createdAt) {
    const date = new Date(createdAt);
    const userId = parseInt(selectedUserId)
    const messageClass = recipientId === userId ? 'chat-message-right' : 'chat-message-left';
    const messageBackground = recipientId === userId ? 'msg-bg' : 'interlocutor-bg';

    return '<div class="' + messageClass + ' pb-4"><div class="flex-shrink-1 ' + messageBackground + ' rounded py-1 px-3 mr-3" style="white-space: pre-line"><p>' + content + '</p> <div class="text-muted small text-nowrap mt-2">' + date.toLocaleString() + '</div></div></div></div>'
}

function startMessagePolling(userId) {
    clearInterval(messagePollingInterval);

    messagePollingInterval = setInterval(async () => {
        await loadMessages(userId);
    }, 1000);

}

async function fetchUsers() {
    try {
        const response = await axios.get('auth/users/');
        const users = response.data;
        const userList = $("#interlocutors");

        userList.empty();

        users.forEach(user => {
            userList.append(`
                <div data-user-id="${user.id}" class="list-group-item list-group-item-action border-0">
                    <div class="d-flex align-items-start">
                        <div class="flex-grow-1 ml-3">
                            <p class="m-0">${user.name}</p>
                        </div>
                    </div>
                </div>
            `);
        });
    } catch (error) {
        console.error(`Error fetching users: ${error}`);
    }
}

$(document).on('click', '.list-group-item', function () {
    selectUser($(this).data('user-id'), $(this).find('p').text());
});

sendBtn.on('click', sendMessage);

document.addEventListener('DOMContentLoaded', fetchUsers);
setInterval(fetchUsers, 10000);

