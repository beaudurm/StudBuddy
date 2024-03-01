const APP_ID = 'cb3fa3b62ac94450847c7b1c7d2e35b1'
const  CHANNEL = 'main'
const  TOKEN = '007eJxTYEj1LffgFftzIs5sw9zui/PN+L6uKdnJqsdnoZtjujp7xw0FhuQk47RE4yQzo8RkSxMTUwMLE/Nk8yTDZPMUo1Rj0yRD/9cPUxsCGRk2Gq9kYWSAQBCfhSE3MTOPgQEA8NIevA=='
let UID;

const client = AgoraRTC.createClient({mode: 'rtc', codec: 'vp8'})
let localTracks = []
let remoteUsers = {}

let joinAndDisplayLocalStream = async () => {
    client.on('user-published', handleUserJoined) 
    client.on('user-left', handleUserLeft) 
       
    
    UID = await client.join(APP_ID, CHANNEL, TOKEN, null)

    localTracks = await AgoraRTC.createMicrophoneAndCameraTracks()

    let player = ` <div class="video-container" id="user container-${UID}">
                        <div class="username-wrapper"><span class="user-name">My Name</span></div>
                        <div class="video-player" id="user-${UID}"></div>
                </div>`
    document.getElementById('video-streams').insertAdjacentHTML('beforeend', player)

    localTracks[1].play(`user-${UID}`)

    await client.publish([localTracks[0], localTracks [1]])

}

let handleUserJoined = async (user, mediaType) => {
    remoteUsers[user.uid] = user
    await client.subscribe(user, mediaType)

    if(mediaType === 'video'){
        let player = document.getElementById(`user-container-${user.uid}`)
        if (player != null){
            player.remove()
        }

        player = ` <div class="video-container" id="user container-${user.uid}">
        <div class="username-wrapper"><span class="user-name">My Name</span></div>
        <div class="video-player" id="user-${user.uid}"></div>
        </div>`
        document.getElementById('video-streams').insertAdjacentHTML('beforeend', player)
        user.videoTrack.play(`user-${user.uid}`)
        }

        if(mediaType === 'audio'){
            user.audioTrack.play()
    }
}

let handleUserLeft = async (user) => {
    delete remoteUsers[user.uid]
    document.getElementById(`user-container-${user.uid}`).remove()
}

joinAndDisplayLocalStream()